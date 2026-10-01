"""
Phase 1: Lesion Frequency Analysis for Gabor Filter Initialization.

Scientific justification for LitchiHybridNet's Gabor branch design.
Analyzes spatial frequency content of leaf lesion regions vs. healthy tissue to:
1. Identify dominant spatial frequencies (wavelengths) per disease class
2. Identify dominant orientations per disease class  
3. Provide data-driven initialization for the LearnableGaborConv2d layer
4. Generate publication-quality figures (PSD, orientation histograms, Gabor responses)
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from PIL import Image
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "figures"
DATA_DIR = PROJECT_ROOT.parent / "Dataset" / "Dataset"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"

SAMPLES_PER_CLASS = 50  # Images to analyze per class
IMG_SIZE = 256


def segment_lesion_mask(image_rgb: np.ndarray) -> np.ndarray:
    """
    Simple lesion segmentation using HSV + Lab color space thresholding.
    Identifies diseased regions (brown, yellow, dark spots) vs. healthy green.
    Returns binary mask: 1 = lesion, 0 = healthy/background.
    """
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    
    # Healthy green leaves: H in [30, 85], high S, medium V
    green_mask = (
        (hsv[:, :, 0] >= 30) & (hsv[:, :, 0] <= 85) &
        (hsv[:, :, 1] >= 30) &
        (hsv[:, :, 2] >= 30)
    )
    
    # Leaf region (not background) - use Lab brightness
    leaf_mask = lab[:, :, 0] > 30  # Not too dark (background)
    
    # Lesion = leaf area that is NOT green
    lesion_mask = leaf_mask & (~green_mask)
    
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    lesion_mask = lesion_mask.astype(np.uint8)
    lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    return lesion_mask


def compute_radial_psd(gray_patch: np.ndarray) -> tuple:
    """
    Compute radial Power Spectral Density of a grayscale image patch.
    Returns (frequencies, radial_psd).
    """
    h, w = gray_patch.shape
    
    # Apply Hanning window to reduce spectral leakage
    win_h = np.hanning(h)
    win_w = np.hanning(w)
    window = np.outer(win_h, win_w)
    
    windowed = gray_patch * window
    
    # 2D FFT
    fft = np.fft.fft2(windowed)
    fft_shift = np.fft.fftshift(fft)
    psd = np.abs(fft_shift) ** 2
    
    # Radial average
    cy, cx = h // 2, w // 2
    Y, X = np.ogrid[:h, :w]
    R = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2).astype(int)
    
    max_r = min(cy, cx)
    radial_psd = np.zeros(max_r)
    for r in range(max_r):
        mask = R == r
        if mask.sum() > 0:
            radial_psd[r] = psd[mask].mean()
    
    # Convert to spatial frequency (cycles per pixel)
    freqs = np.arange(max_r) / max_r
    
    return freqs, radial_psd


def compute_orientation_histogram(gray_patch: np.ndarray, n_bins: int = 36) -> np.ndarray:
    """
    Compute orientation histogram using gradient-based approach.
    Returns histogram of dominant gradient orientations (0-180 degrees).
    """
    # Sobel gradients
    gx = cv2.Sobel(gray_patch, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_patch, cv2.CV_64F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * 180 / np.pi  # [-180, 180]
    orientation = orientation % 180  # Map to [0, 180)
    
    # Weighted histogram (magnitude as weight)
    hist, bin_edges = np.histogram(
        orientation.ravel(),
        bins=n_bins,
        range=(0, 180),
        weights=magnitude.ravel()
    )
    
    return hist / (hist.sum() + 1e-8)


def analyze_class_frequencies(
    data_dir: Path,
    class_name: str,
    n_samples: int = SAMPLES_PER_CLASS,
) -> dict:
    """Analyze frequency content for one disease class."""
    class_dir = data_dir / class_name
    files = sorted([f for f in class_dir.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png'}])
    
    if len(files) > n_samples:
        rng = np.random.RandomState(42)
        indices = rng.choice(len(files), n_samples, replace=False)
        files = [files[i] for i in indices]
    
    all_lesion_psd = []
    all_healthy_psd = []
    all_lesion_orient = []
    lesion_fractions = []
    
    for fpath in files:
        try:
            img = cv2.imread(str(fpath))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(float)
            
            mask = segment_lesion_mask(img)
            lesion_frac = mask.sum() / mask.size
            lesion_fractions.append(lesion_frac)
            
            # Compute PSD on full image
            freqs, psd = compute_radial_psd(gray)
            
            if lesion_frac > 0.05:  # At least 5% lesion area
                # Lesion region PSD
                lesion_gray = gray.copy()
                lesion_gray[mask == 0] = 0
                _, lesion_psd = compute_radial_psd(lesion_gray)
                all_lesion_psd.append(lesion_psd)
                
                # Orientation of lesion edges
                orient_hist = compute_orientation_histogram(
                    (gray * mask).astype(np.uint8)
                )
                all_lesion_orient.append(orient_hist)
            
            # Healthy region PSD
            healthy_mask = (mask == 0) & (gray > 30)
            if healthy_mask.sum() > 100:
                healthy_gray = gray.copy()
                healthy_gray[~healthy_mask] = 0
                _, healthy_psd = compute_radial_psd(healthy_gray)
                all_healthy_psd.append(healthy_psd)
                
        except Exception as e:
            continue
    
    result = {
        "class_name": class_name,
        "n_analyzed": len(files),
        "mean_lesion_fraction": float(np.mean(lesion_fractions)) if lesion_fractions else 0,
    }
    
    if all_lesion_psd:
        min_len = min(len(p) for p in all_lesion_psd)
        lesion_psd_arr = np.array([p[:min_len] for p in all_lesion_psd])
        result["lesion_psd_mean"] = lesion_psd_arr.mean(axis=0).tolist()
        result["lesion_psd_std"] = lesion_psd_arr.std(axis=0).tolist()
        
        # Find dominant spatial frequency (wavelength)
        mean_psd = lesion_psd_arr.mean(axis=0)
        # Skip DC (index 0) and very low frequencies
        start_idx = max(3, len(mean_psd) // 20)
        peak_idx = start_idx + np.argmax(mean_psd[start_idx:])
        
        # Convert frequency index to approximate wavelength in pixels
        dominant_freq = peak_idx / min_len
        dominant_wavelength = 1.0 / (dominant_freq + 1e-8)
        result["dominant_freq_idx"] = int(peak_idx)
        result["dominant_wavelength_px"] = float(dominant_wavelength)
    
    if all_lesion_orient:
        orient_arr = np.array(all_lesion_orient)
        result["orientation_hist_mean"] = orient_arr.mean(axis=0).tolist()
        
        # Dominant orientation
        mean_orient = orient_arr.mean(axis=0)
        dominant_bin = np.argmax(mean_orient)
        dominant_angle = dominant_bin * 180 / len(mean_orient)
        result["dominant_orientation_deg"] = float(dominant_angle)
    
    if all_healthy_psd:
        min_len_h = min(len(p) for p in all_healthy_psd)
        healthy_psd_arr = np.array([p[:min_len_h] for p in all_healthy_psd])
        result["healthy_psd_mean"] = healthy_psd_arr.mean(axis=0).tolist()
    
    return result


def plot_psd_comparison(all_results: list, save_path: Path):
    """Plot mean radial PSD per class (lesion vs healthy)."""
    fig, axes = plt.subplots(3, 4, figsize=(18, 12))
    axes = axes.flatten()
    colors = plt.cm.Set3(np.linspace(0, 1, 11))
    
    for i, result in enumerate(all_results):
        ax = axes[i]
        cls = result["class_name"]
        
        if "lesion_psd_mean" in result:
            psd = np.array(result["lesion_psd_mean"])
            freqs = np.linspace(0, 0.5, len(psd))
            ax.semilogy(freqs[1:], psd[1:], color="red", label="Lesion", linewidth=1.5)
        
        if "healthy_psd_mean" in result:
            psd_h = np.array(result["healthy_psd_mean"])
            freqs_h = np.linspace(0, 0.5, len(psd_h))
            ax.semilogy(freqs_h[1:], psd_h[1:], color="green", label="Healthy", linewidth=1.5, alpha=0.7)
        
        ax.set_title(cls, fontsize=10, fontweight="bold")
        ax.set_xlabel("Spatial Freq", fontsize=8)
        ax.set_ylabel("PSD", fontsize=8)
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
    
    # Hide last subplot if 11 classes
    if len(all_results) < len(axes):
        for j in range(len(all_results), len(axes)):
            axes[j].set_visible(False)
    
    fig.suptitle("Lesion vs Healthy Tissue: Radial Power Spectral Density per Class",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def plot_orientation_histograms(all_results: list, save_path: Path):
    """Plot orientation histograms per class."""
    fig, axes = plt.subplots(3, 4, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, result in enumerate(all_results):
        ax = axes[i]
        cls = result["class_name"]
        
        if "orientation_hist_mean" in result:
            hist = np.array(result["orientation_hist_mean"])
            angles = np.linspace(0, 180, len(hist), endpoint=False)
            ax.bar(angles, hist, width=180/len(hist)*0.8, color="steelblue", edgecolor="black", linewidth=0.3)
            
            if "dominant_orientation_deg" in result:
                dom = result["dominant_orientation_deg"]
                ax.axvline(dom, color="red", linestyle="--", linewidth=2, label=f"Dominant: {dom:.0f} deg")
                ax.legend(fontsize=7)
        
        ax.set_title(cls, fontsize=10, fontweight="bold")
        ax.set_xlabel("Orientation (deg)", fontsize=8)
        ax.set_ylabel("Magnitude", fontsize=8)
        ax.set_xlim(0, 180)
    
    if len(all_results) < len(axes):
        for j in range(len(all_results), len(axes)):
            axes[j].set_visible(False)
    
    fig.suptitle("Lesion Edge Orientation Distribution per Disease Class",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def plot_wavelength_summary(all_results: list, save_path: Path):
    """Bar chart of dominant wavelengths and orientations per class."""
    classes, wavelengths, orientations, lesion_fracs = [], [], [], []
    
    for r in all_results:
        classes.append(r["class_name"])
        wavelengths.append(r.get("dominant_wavelength_px", 0))
        orientations.append(r.get("dominant_orientation_deg", 0))
        lesion_fracs.append(r.get("mean_lesion_fraction", 0))
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Wavelengths
    x = np.arange(len(classes))
    axes[0].barh(x, wavelengths, color="coral", edgecolor="black")
    axes[0].set_yticks(x)
    axes[0].set_yticklabels(classes, fontsize=9)
    axes[0].set_xlabel("Dominant Wavelength (px)", fontsize=11)
    axes[0].set_title("Dominant Spatial Wavelength", fontsize=12, fontweight="bold")
    axes[0].grid(axis="x", alpha=0.3)
    
    # Orientations
    axes[1].barh(x, orientations, color="steelblue", edgecolor="black")
    axes[1].set_yticks(x)
    axes[1].set_yticklabels(classes, fontsize=9)
    axes[1].set_xlabel("Dominant Orientation (degrees)", fontsize=11)
    axes[1].set_title("Dominant Edge Orientation", fontsize=12, fontweight="bold")
    axes[1].grid(axis="x", alpha=0.3)
    
    # Lesion fraction
    axes[2].barh(x, [f * 100 for f in lesion_fracs], color="forestgreen", edgecolor="black")
    axes[2].set_yticks(x)
    axes[2].set_yticklabels(classes, fontsize=9)
    axes[2].set_xlabel("Mean Lesion Area (%)", fontsize=11)
    axes[2].set_title("Lesion Coverage", fontsize=12, fontweight="bold")
    axes[2].grid(axis="x", alpha=0.3)
    
    fig.suptitle("Lesion Frequency Signature Summary — Gabor Filter Initialization Basis",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


def derive_gabor_init_params(all_results: list) -> dict:
    """
    Derive initial Gabor parameters from frequency analysis.
    Maps dominant wavelengths and orientations to filter bank initialization.
    """
    wavelengths = [r.get("dominant_wavelength_px", 8) for r in all_results if r.get("dominant_wavelength_px", 0) > 0]
    orientations = [r.get("dominant_orientation_deg", 0) for r in all_results if "dominant_orientation_deg" in r]
    
    # Scale wavelengths from pixel units to kernel-relative (for 224px input resized)
    scale_factor = IMG_SIZE / 224.0
    scaled_wavelengths = [w / scale_factor for w in wavelengths]
    
    # Determine lambda range
    if scaled_wavelengths:
        min_lambda = max(2.5, np.percentile(scaled_wavelengths, 10))
        max_lambda = min(20.0, np.percentile(scaled_wavelengths, 90))
    else:
        min_lambda, max_lambda = 3.0, 15.0
    
    # Determine orientations to use (cluster dominant orientations)
    if orientations:
        # Use 6 evenly spaced orientations covering the dominant range
        orientation_range = (min(orientations), max(orientations))
    else:
        orientation_range = (0, 150)
    
    init_params = {
        "num_scales": 4,
        "num_orientations": 6,
        "min_lambda": round(float(min_lambda), 2),
        "max_lambda": round(float(max_lambda), 2),
        "init_lambdas": [round(float(l), 2) for l in np.linspace(min_lambda, max_lambda, 4)],
        "init_thetas_deg": [round(float(t), 1) for t in np.linspace(0, 150, 6)],
        "sigma_ratio": 0.56,
        "gamma": 0.5,
        "wavelength_stats": {
            "raw_wavelengths": [round(w, 2) for w in wavelengths],
            "scaled_wavelengths": [round(w, 2) for w in scaled_wavelengths],
        },
        "orientation_stats": {
            "dominant_orientations_deg": [round(o, 1) for o in orientations],
        },
    }
    
    return init_params


def main():
    print("=" * 70)
    print(" PHASE 1: Lesion Frequency Analysis")
    print("=" * 70)
    
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    classes = sorted([d.name for d in DATA_DIR.iterdir() if d.is_dir()])
    print(f"Analyzing {len(classes)} classes with {SAMPLES_PER_CLASS} samples each...\n")
    
    all_results = []
    for cls in tqdm(classes, desc="Analyzing classes"):
        result = analyze_class_frequencies(DATA_DIR, cls, n_samples=SAMPLES_PER_CLASS)
        all_results.append(result)
        print(f"  {cls}: lesion_frac={result['mean_lesion_fraction']:.3f}, "
              f"wavelength={result.get('dominant_wavelength_px', 'N/A')}, "
              f"orientation={result.get('dominant_orientation_deg', 'N/A')}")
    
    # Generate figures
    print("\nGenerating frequency analysis figures...")
    plot_psd_comparison(all_results, FIGURES_DIR / "frequency_psd_comparison.png")
    plot_orientation_histograms(all_results, FIGURES_DIR / "orientation_histograms.png")
    plot_wavelength_summary(all_results, FIGURES_DIR / "wavelength_summary.png")
    
    # Derive Gabor init params
    gabor_init = derive_gabor_init_params(all_results)
    
    # Save results
    output = {
        "per_class_analysis": all_results,
        "gabor_initialization": gabor_init,
    }
    
    output_path = PROJECT_ROOT / "data" / "frequency_analysis.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=4)
    
    print(f"\nGabor initialization parameters derived:")
    print(f"  Lambda range: [{gabor_init['min_lambda']}, {gabor_init['max_lambda']}]")
    print(f"  Init lambdas: {gabor_init['init_lambdas']}")
    print(f"  Init thetas:  {gabor_init['init_thetas_deg']} deg")
    print(f"\nSaved to: {output_path}")
    print("=" * 70)
    print(" PHASE 1 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
