"""
Dataset and DataLoader utilities for LitchiHybridNet.

Features:
- Loads from pre-computed CSV splits (from Phase 0 audit)
- Albumentations-based augmentation pipeline (field conditions)
- Class-weighted sampling for imbalanced data
- Reproducible with fixed seeds
"""

import os
from pathlib import Path
from typing import Tuple, List, Dict, Optional

import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2


LITCHI_CLASSES = [
    "Black Spot",
    "Burned Leaf",
    "Dried Leaf",
    "Fungal Stripe Damage",
    "Healthy Leaf",
    "Insect Chewing Damage",
    "Leaf Blight Disease",
    "Pest-Affected Dry Leaf",
    "Red Rust Disease",
    "White Spot",
    "Yellow Mosaic Virus",
]


class LitchiDataset(Dataset):
    """PyTorch Dataset for BDLitchi, loading from CSV split files."""
    
    def __init__(
        self,
        csv_path: str,
        class_names: Optional[List[str]] = None,
        transform=None,
    ):
        self.df = pd.read_csv(csv_path)
        self.transform = transform
        
        if class_names is None:
            class_names = sorted(self.df["class_name"].unique().tolist())
        self.class_names = class_names
        self.class_to_idx = {name: i for i, name in enumerate(class_names)}
        
        self.samples = [
            (row["path"], self.class_to_idx[row["class_name"]])
            for _, row in self.df.iterrows()
        ]
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, label = self.samples[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.transform is not None:
            augmented = self.transform(image=image)
            image = augmented["image"]
        
        return image, label
    
    def get_labels(self) -> List[int]:
        """Returns all labels for weighted sampling."""
        return [label for _, label in self.samples]
    
    def get_class_counts(self) -> Dict[str, int]:
        """Returns per-class sample counts."""
        return dict(self.df["class_name"].value_counts())


def get_train_transforms(img_size: int = 224) -> A.Compose:
    """
    Training augmentation pipeline for field-condition robustness.
    Simulates real-world variations: lighting, rotation, blur, occlusion.
    """
    return A.Compose([
        A.Resize(img_size, img_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.Rotate(limit=20, border_mode=cv2.BORDER_REFLECT_101, p=0.5),
        A.OneOf([
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0),
            A.HueSaturationValue(hue_shift_limit=15, sat_shift_limit=20, val_shift_limit=15, p=1.0),
        ], p=0.5),
        A.OneOf([
            A.GaussianBlur(blur_limit=(3, 5), p=1.0),
            A.MotionBlur(blur_limit=3, p=1.0),
        ], p=0.2),
        A.CoarseDropout(
            num_holes_range=(1, 6),
            hole_height_range=(int(img_size * 0.03), int(img_size * 0.08)),
            hole_width_range=(int(img_size * 0.03), int(img_size * 0.08)),
            p=0.3
        ),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])


def get_eval_transforms(img_size: int = 224) -> A.Compose:
    """Evaluation transforms: resize and normalize only."""
    return A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])


def get_dataloaders(
    splits_dir: str,
    batch_size: int = 32,
    img_size: int = 224,
    num_workers: int = 0,
    use_class_weights: bool = True,
    class_names: Optional[List[str]] = None,
) -> Tuple[DataLoader, DataLoader, DataLoader, List[str], Dict[str, int]]:
    """
    Creates Train, Validation, and Test DataLoaders from pre-split CSVs.
    
    Returns:
        (train_loader, val_loader, test_loader, class_names, split_counts)
    """
    splits_dir = Path(splits_dir)
    
    train_transform = get_train_transforms(img_size)
    eval_transform = get_eval_transforms(img_size)
    
    train_ds = LitchiDataset(str(splits_dir / "train.csv"), class_names=class_names, transform=train_transform)
    val_ds = LitchiDataset(str(splits_dir / "val.csv"), class_names=class_names, transform=eval_transform)
    test_ds = LitchiDataset(str(splits_dir / "test.csv"), class_names=class_names, transform=eval_transform)
    
    class_names = train_ds.class_names
    
    split_counts = {
        "train": len(train_ds),
        "val": len(val_ds),
        "test": len(test_ds),
        "total": len(train_ds) + len(val_ds) + len(test_ds),
    }
    
    # Weighted sampling for class imbalance
    train_sampler = None
    shuffle_train = True
    if use_class_weights:
        labels = train_ds.get_labels()
        class_counts = np.bincount(labels)
        weights = 1.0 / class_counts[labels]
        train_sampler = WeightedRandomSampler(weights, num_samples=len(labels), replacement=True)
        shuffle_train = False  # sampler handles shuffling
    
    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=shuffle_train,
        sampler=train_sampler, num_workers=num_workers, pin_memory=False, drop_last=True
    )
    val_loader = DataLoader(
        val_ds, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=False
    )
    test_loader = DataLoader(
        test_ds, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=False
    )
    
    return train_loader, val_loader, test_loader, class_names, split_counts
