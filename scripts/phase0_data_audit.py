"""
Phase 0: Data Acquisition and Audit for BDLitchi Dataset.

Performs:
1. Dataset scanning (class names, counts, formats, resolutions)
2. Corrupt file detection
3. Near-duplicate detection using perceptual hashing (pHash, dHash)
4. Group-aware stratified splitting (70/15/15)
5. Generates audit figures (class distribution, resolution scatter, sample grid)
6. Saves splits to CSV for reproducibility
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Tuple, Dict, Set

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split

# Try imagehash; fall back to manual if not available
try:
    import imagehash
    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False
    print("WARNING: imagehash not installed, using MD5 exact-duplicate detection only")


# ─── Configuration ─────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = PROJECT_ROOT.parent / "Dataset" / "Dataset"  # original dataset
DATA_AUG_DIR = PROJECT_ROOT.parent / "Litchi_Augmented" / "Litchi_Augmented"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
FIGURES_DIR = PROJECT_ROOT / "figures"
AUDIT_DIR = PROJECT_ROOT / "data" / "audit"

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
RANDOM_STATE = 42
TEST_RATIO = 0.15
VAL_RATIO = 0.15

# pHash Hamming distance threshold for near-duplicates
PHASH_THRESHOLD = 8  # bits; images within this distance are "near-duplicates"


def scan_dataset(data_dir: Path) -> pd.DataFrame:
    """Scan dataset directory and return DataFrame with image metadata."""
    records = []
    for class_dir in sorted(data_dir.iterdir()):
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        for img_file in class_dir.iterdir():
            if img_file.suffix.lower() in VALID_EXTENSIONS:
                records.append({
                    "path": str(img_file),
                    "filename": img_file.name,
                    "class_name": class_name,
                    "extension": img_file.suffix.lower(),
                    "file_size_kb": img_file.stat().st_size / 1024,
                })
    return pd.DataFrame(records)


def check_image_integrity(df: pd.DataFrame) -> pd.DataFrame:
    """Check each image can be opened and read its dimensions."""
    widths, heights, corrupt = [], [], []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Checking image integrity"):
        try:
            with Image.open(row["path"]) as img:
                img.verify()
            # Re-open after verify (verify can close)
            with Image.open(row["path"]) as img:
                w, h = img.size
            widths.append(w)
            heights.append(h)
            corrupt.append(False)
        except Exception as e:
            widths.append(None)
            heights.append(None)
            corrupt.append(True)
    
    df = df.copy()
    df["width"] = widths
    df["height"] = heights
    df["corrupt"] = corrupt
    return df


def compute_hashes(df: pd.DataFrame) -> pd.DataFrame:
    """Compute perceptual hashes and MD5 for duplicate detection."""
    md5_list, phash_list, dhash_list = [], [], []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Computing hashes"):
        path = row["path"]
        
        # MD5 (exact duplicate detection)
        with open(path, "rb") as f:
            md5_list.append(hashlib.md5(f.read()).hexdigest())
        
        if HAS_IMAGEHASH and not row.get("corrupt", False):
            try:
                img = Image.open(path).convert("RGB")
                phash_list.append(str(imagehash.phash(img, hash_size=16)))
                dhash_list.append(str(imagehash.dhash(img, hash_size=16)))
            except:
                phash_list.append(None)
                dhash_list.append(None)
        else:
            phash_list.append(None)
            dhash_list.append(None)
    
    df = df.copy()
    df["md5"] = md5_list
    df["phash"] = phash_list
    df["dhash"] = dhash_list
    return df


def find_duplicate_groups(df: pd.DataFrame, hash_col: str = "phash", threshold: int = PHASH_THRESHOLD) -> Dict[int, List[int]]:
    """
    Find groups of near-duplicate images using perceptual hashing.
    
    Fast approach: 
    1. First find exact hash matches (O(n) via dict bucketing)
    2. Then compare within each class only for near-duplicates (much smaller groups)
    Returns dict: group_id -> list of row indices.
    """
    if hash_col not in df.columns or df[hash_col].isna().all():
        print("Using MD5 exact-duplicate grouping (no perceptual hashes)")
        groups = {}
        md5_to_group = {}
        group_id = 0
        for idx, row in df.iterrows():
            md5 = row["md5"]
            if md5 in md5_to_group:
                groups[md5_to_group[md5]].append(idx)
            else:
                md5_to_group[md5] = group_id
                groups[group_id] = [idx]
                group_id += 1
        return groups
    
    valid = df[df[hash_col].notna()].copy()
    
    # Union-Find
    parent = {idx: idx for idx in valid.index}
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    
    # Step 1: Exact hash matches (O(n) bucketing)
    hash_buckets = defaultdict(list)
    for idx, row in valid.iterrows():
        hash_buckets[row[hash_col]].append(idx)
    
    exact_dup_count = 0
    for h, members in hash_buckets.items():
        if len(members) > 1:
            for m in members[1:]:
                union(members[0], m)
            exact_dup_count += len(members) - 1
    print(f"  Exact hash duplicates: {exact_dup_count}")
    
    # Step 2: Near-duplicate comparison WITHIN each class only
    # This reduces O(n^2) to O(sum(class_size^2)) which is much smaller
    if threshold > 0:
        classes = valid["class_name"].unique()
        total_near = 0
        for cls in tqdm(classes, desc="Near-duplicate detection (per-class)"):
            cls_mask = valid["class_name"] == cls
            cls_indices = valid[cls_mask].index.tolist()
            cls_hashes = [(idx, imagehash.hex_to_hash(valid.loc[idx, hash_col])) for idx in cls_indices]
            
            n = len(cls_hashes)
            for i in range(n):
                for j in range(i + 1, n):
                    idx_i, h_i = cls_hashes[i]
                    idx_j, h_j = cls_hashes[j]
                    if h_i - h_j <= threshold:
                        if find(idx_i) != find(idx_j):
                            union(idx_i, idx_j)
                            total_near += 1
        print(f"  Near-duplicate pairs found: {total_near}")
    
    # Collect groups
    groups_map = defaultdict(list)
    for idx in valid.index:
        groups_map[find(idx)].append(idx)
    
    groups = {}
    for gid, (_, members) in enumerate(groups_map.items()):
        groups[gid] = members
    
    return groups


def group_aware_stratified_split(
    df: pd.DataFrame, 
    dup_groups: Dict[int, List[int]],
    test_ratio: float = TEST_RATIO,
    val_ratio: float = VAL_RATIO,
    random_state: int = RANDOM_STATE
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split dataset ensuring duplicate groups stay in the same split.
    """
    # Assign group IDs to each sample
    idx_to_group = {}
    for gid, members in dup_groups.items():
        for idx in members:
            idx_to_group[idx] = gid
    
    df = df.copy()
    df["dup_group"] = df.index.map(lambda x: idx_to_group.get(x, -x))
    
    # Get unique groups with their class labels (majority vote)
    group_info = []
    for gid in df["dup_group"].unique():
        group_df = df[df["dup_group"] == gid]
        class_name = group_df["class_name"].mode().iloc[0]
        group_info.append({"group_id": gid, "class_name": class_name, "count": len(group_df)})
    
    group_df = pd.DataFrame(group_info)
    
    # Stratified split on groups
    train_val_groups, test_groups = train_test_split(
        group_df["group_id"].values,
        test_size=test_ratio,
        stratify=group_df["class_name"].values,
        random_state=random_state
    )
    
    # Get class labels for train_val groups
    train_val_df = group_df[group_df["group_id"].isin(train_val_groups)]
    val_rel_size = val_ratio / (1.0 - test_ratio)
    
    train_groups, val_groups = train_test_split(
        train_val_df["group_id"].values,
        test_size=val_rel_size,
        stratify=train_val_df["class_name"].values,
        random_state=random_state
    )
    
    # Map back to samples
    train_set = set(train_groups)
    val_set = set(val_groups)
    test_set = set(test_groups)
    
    train_mask = df["dup_group"].isin(train_set)
    val_mask = df["dup_group"].isin(val_set)
    test_mask = df["dup_group"].isin(test_set)
    
    return df[train_mask].copy(), df[val_mask].copy(), df[test_mask].copy()


def plot_class_distribution(df: pd.DataFrame, save_path: Path, title: str = "BDLitchi"):
    """Bar chart of class distribution."""
    counts = df["class_name"].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette("husl", len(counts))
    bars = ax.bar(range(len(counts)), counts.values, color=colors, edgecolor="black", linewidth=0.5)
    
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=40, ha="right", fontsize=10)
    ax.set_ylabel("Number of Images", fontsize=12, fontweight="bold")
    ax.set_title(f"{title}: Class Distribution ({len(df):,} total images)", fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    
    # Annotate counts
    for bar, count in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15, 
                str(count), ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    # Imbalance ratio
    imbalance = counts.max() / counts.min()
    ax.text(0.98, 0.95, f"Imbalance ratio: {imbalance:.2f}:1", transform=ax.transAxes,
            ha="right", va="top", fontsize=10, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def plot_resolution_scatter(df: pd.DataFrame, save_path: Path):
    """Scatter plot of image resolutions."""
    valid = df[~df["corrupt"]].copy()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    classes = sorted(valid["class_name"].unique())
    colors = sns.color_palette("husl", len(classes))
    
    for cls, color in zip(classes, colors):
        subset = valid[valid["class_name"] == cls]
        ax.scatter(subset["width"], subset["height"], c=[color], label=cls,
                   alpha=0.4, s=15, edgecolors="none")
    
    ax.set_xlabel("Width (px)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Height (px)", fontsize=12, fontweight="bold")
    ax.set_title("BDLitchi: Image Resolution Distribution", fontsize=14, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right", ncol=2)
    ax.grid(True, linestyle="--", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def plot_sample_grid(df: pd.DataFrame, save_path: Path, samples_per_class: int = 3):
    """Grid of sample images per class."""
    classes = sorted(df["class_name"].unique())
    n_classes = len(classes)
    
    fig, axes = plt.subplots(n_classes, samples_per_class, figsize=(4 * samples_per_class, 3.5 * n_classes))
    fig.suptitle("BDLitchi: Sample Images per Disease Class", fontsize=16, fontweight="bold", y=1.01)
    
    for i, cls in enumerate(classes):
        cls_df = df[df["class_name"] == cls].sample(n=min(samples_per_class, len(df[df["class_name"] == cls])),
                                                       random_state=RANDOM_STATE)
        for j in range(samples_per_class):
            ax = axes[i, j] if n_classes > 1 else axes[j]
            if j < len(cls_df):
                img_path = cls_df.iloc[j]["path"]
                try:
                    img = Image.open(img_path).convert("RGB")
                    ax.imshow(img)
                except:
                    ax.text(0.5, 0.5, "Error", ha="center", va="center")
            ax.axis("off")
            if j == 0:
                ax.set_title(cls, fontsize=10, fontweight="bold", loc="left")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def plot_split_distribution(train_df, val_df, test_df, save_path: Path):
    """Stacked bar chart showing split distribution per class."""
    classes = sorted(set(train_df["class_name"].unique()))
    
    train_counts = train_df["class_name"].value_counts().reindex(classes, fill_value=0)
    val_counts = val_df["class_name"].value_counts().reindex(classes, fill_value=0)
    test_counts = test_df["class_name"].value_counts().reindex(classes, fill_value=0)
    
    x = np.arange(len(classes))
    width = 0.6
    
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(x, train_counts.values, width, label=f"Train ({len(train_df):,})", color="#2196F3", alpha=0.9)
    ax.bar(x, val_counts.values, width, bottom=train_counts.values, label=f"Val ({len(val_df):,})", color="#FF9800", alpha=0.9)
    ax.bar(x, test_counts.values, width, bottom=train_counts.values + val_counts.values, label=f"Test ({len(test_df):,})", color="#4CAF50", alpha=0.9)
    
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=40, ha="right", fontsize=10)
    ax.set_ylabel("Number of Images", fontsize=12, fontweight="bold")
    ax.set_title("BDLitchi: Group-Aware Stratified Split Distribution (70/15/15)", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def main():
    print("=" * 70)
    print(" PHASE 0: BDLitchi Data Audit and Splitting")
    print("=" * 70)
    
    # Create output dirs
    for d in [SPLITS_DIR, FIGURES_DIR, AUDIT_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    # ─── 1. Scan Dataset ───────────────────────────────────────────────
    print("\n[1/7] Scanning dataset directory...")
    if not DATA_RAW_DIR.exists():
        print(f"ERROR: Dataset not found at {DATA_RAW_DIR}")
        print("Please download BDLitchi from: https://data.mendeley.com/datasets/jhb24mszdk/1")
        sys.exit(1)
    
    df = scan_dataset(DATA_RAW_DIR)
    print(f"  Found {len(df):,} images across {df['class_name'].nunique()} classes")
    print(f"  Classes: {sorted(df['class_name'].unique())}")
    print(f"  Extensions: {dict(df['extension'].value_counts())}")
    
    # ─── 2. Check Integrity ────────────────────────────────────────────
    print("\n[2/7] Checking image integrity...")
    df = check_image_integrity(df)
    n_corrupt = df["corrupt"].sum()
    print(f"  Corrupt files: {n_corrupt}")
    if n_corrupt > 0:
        print(f"  Corrupt files:\n{df[df['corrupt']]['path'].tolist()}")
    
    # Remove corrupt files
    df = df[~df["corrupt"]].reset_index(drop=True)
    
    # Resolution stats
    print(f"\n  Resolution Statistics:")
    print(f"    Width  — min: {df['width'].min()}, max: {df['width'].max()}, median: {df['width'].median()}")
    print(f"    Height — min: {df['height'].min()}, max: {df['height'].max()}, median: {df['height'].median()}")
    unique_res = df.apply(lambda r: f"{int(r['width'])}x{int(r['height'])}", axis=1).nunique()
    print(f"    Unique resolutions: {unique_res}")
    
    # ─── 3. Compute Hashes ─────────────────────────────────────────────
    print("\n[3/7] Computing perceptual hashes for duplicate detection...")
    df = compute_hashes(df)
    
    # Exact duplicates (MD5)
    md5_dups = df[df.duplicated(subset="md5", keep=False)]
    n_exact_dup_groups = md5_dups["md5"].nunique()
    print(f"  Exact duplicate groups (MD5): {n_exact_dup_groups}")
    print(f"  Exact duplicate images: {len(md5_dups)}")
    
    # ─── 4. Near-Duplicate Grouping ────────────────────────────────────
    print("\n[4/7] Finding near-duplicate groups...")
    dup_groups = find_duplicate_groups(df, hash_col="phash", threshold=PHASH_THRESHOLD)
    
    # Stats
    multi_groups = {gid: members for gid, members in dup_groups.items() if len(members) > 1}
    total_in_groups = sum(len(m) for m in multi_groups.values())
    print(f"  Total unique duplicate groups (size > 1): {len(multi_groups)}")
    print(f"  Total images in duplicate groups: {total_in_groups}")
    
    # Check cross-class duplicates
    cross_class = 0
    for gid, members in multi_groups.items():
        classes_in_group = df.loc[members, "class_name"].nunique()
        if classes_in_group > 1:
            cross_class += 1
    print(f"  Cross-class duplicate groups: {cross_class}")
    
    # ─── 5. Group-Aware Stratified Split ───────────────────────────────
    print("\n[5/7] Performing group-aware stratified splitting (70/15/15)...")
    train_df, val_df, test_df = group_aware_stratified_split(df, dup_groups)
    
    print(f"  Train: {len(train_df):,} ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Val:   {len(val_df):,} ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:  {len(test_df):,} ({len(test_df)/len(df)*100:.1f}%)")
    
    # Verify no group leakage
    train_groups = set(train_df["dup_group"].unique())
    val_groups = set(val_df["dup_group"].unique())
    test_groups = set(test_df["dup_group"].unique())
    
    assert len(train_groups & val_groups) == 0, "Group leakage: train & val"
    assert len(train_groups & test_groups) == 0, "Group leakage: train & test"
    assert len(val_groups & test_groups) == 0, "Group leakage: val & test"
    print("  [OK] No duplicate group crosses split boundaries")
    
    # Save splits
    for split_name, split_df in [("train", train_df), ("val", val_df), ("test", test_df)]:
        split_path = SPLITS_DIR / f"{split_name}.csv"
        split_df[["path", "class_name", "dup_group"]].to_csv(split_path, index=False)
        print(f"  Saved: {split_path}")
    
    # ─── 6. Generate Figures ───────────────────────────────────────────
    print("\n[6/7] Generating audit figures...")
    plot_class_distribution(df, FIGURES_DIR / "class_distribution.png")
    plot_resolution_scatter(df, FIGURES_DIR / "resolution_scatter.png")
    plot_sample_grid(df, FIGURES_DIR / "sample_grid.png", samples_per_class=3)
    plot_split_distribution(train_df, val_df, test_df, FIGURES_DIR / "split_distribution.png")
    
    # ─── 7. Save Audit Report ──────────────────────────────────────────
    print("\n[7/7] Saving audit report...")
    
    class_stats = []
    for cls in sorted(df["class_name"].unique()):
        cls_df = df[df["class_name"] == cls]
        class_stats.append({
            "class": cls,
            "count": len(cls_df),
            "pct": f"{len(cls_df)/len(df)*100:.1f}%",
            "mean_width": int(cls_df["width"].mean()),
            "mean_height": int(cls_df["height"].mean()),
            "mean_size_kb": f"{cls_df['file_size_kb'].mean():.1f}",
            "train": len(train_df[train_df["class_name"] == cls]),
            "val": len(val_df[val_df["class_name"] == cls]),
            "test": len(test_df[test_df["class_name"] == cls]),
        })
    
    audit_report = {
        "dataset": "BDLitchi: Bangladeshi Litchi Leaf Disease Dataset",
        "source": "https://data.mendeley.com/datasets/jhb24mszdk/1",
        "total_images": len(df),
        "num_classes": df["class_name"].nunique(),
        "classes": sorted(df["class_name"].unique().tolist()),
        "class_statistics": class_stats,
        "corrupt_files": int(n_corrupt),
        "extensions": dict(df["extension"].value_counts()),
        "resolution": {
            "width_range": [int(df["width"].min()), int(df["width"].max())],
            "height_range": [int(df["height"].min()), int(df["height"].max())],
            "unique_resolutions": int(unique_res),
        },
        "duplicates": {
            "exact_md5_groups": int(n_exact_dup_groups),
            "exact_md5_images": int(len(md5_dups)),
            "near_duplicate_groups": len(multi_groups),
            "near_duplicate_images": total_in_groups,
            "cross_class_duplicate_groups": cross_class,
            "phash_threshold": PHASH_THRESHOLD,
        },
        "splits": {
            "train": len(train_df),
            "val": len(val_df),
            "test": len(test_df),
            "random_state": RANDOM_STATE,
            "no_group_leakage": True,
        },
    }
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    audit_path = AUDIT_DIR / "dataset_audit.json"
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=4, cls=NumpyEncoder)
    print(f"  Saved: {audit_path}")
    
    # Print summary table
    print("\n" + "=" * 70)
    print(" PHASE 0 COMPLETE: Dataset Audit Summary")
    print("=" * 70)
    stats_df = pd.DataFrame(class_stats)
    print(stats_df.to_string(index=False))
    print(f"\nTotal images: {len(df):,}")
    print(f"Train/Val/Test: {len(train_df):,}/{len(val_df):,}/{len(test_df):,}")
    print(f"Near-duplicate groups: {len(multi_groups)}")
    print(f"Figures saved to: {FIGURES_DIR}")
    print(f"Splits saved to: {SPLITS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
