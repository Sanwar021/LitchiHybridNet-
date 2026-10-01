"""
Training engine for LitchiHybridNet.

Features:
- Config-driven training loop
- AdamW with cosine annealing + warmup
- Label smoothing, optional focal loss
- Early stopping on val macro-F1
- Gradient clipping
- Per-epoch JSON logging
- Checkpoint saving (best + last)
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class FocalLoss(nn.Module):
    """Focal Loss for class imbalance (Lin et al., 2017)."""
    def __init__(self, alpha=None, gamma=2.0, label_smoothing=0.0):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
        self.label_smoothing = label_smoothing
    
    def forward(self, logits, targets):
        ce = nn.functional.cross_entropy(
            logits, targets, weight=self.alpha,
            label_smoothing=self.label_smoothing, reduction='none'
        )
        pt = torch.exp(-ce)
        focal = ((1 - pt) ** self.gamma * ce).mean()
        return focal


class CosineWarmupScheduler:
    """Cosine annealing with linear warmup."""
    def __init__(self, optimizer, warmup_epochs, total_epochs, min_lr=1e-6):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs
        self.min_lr = min_lr
        self.base_lrs = [pg['lr'] for pg in optimizer.param_groups]
    
    def step(self, epoch):
        if epoch < self.warmup_epochs:
            # Linear warmup
            scale = (epoch + 1) / self.warmup_epochs
        else:
            # Cosine decay
            progress = (epoch - self.warmup_epochs) / max(1, self.total_epochs - self.warmup_epochs)
            scale = 0.5 * (1 + np.cos(np.pi * progress))
        
        for pg, base_lr in zip(self.optimizer.param_groups, self.base_lrs):
            pg['lr'] = max(self.min_lr, base_lr * scale)
    
    def get_last_lr(self):
        return [pg['lr'] for pg in self.optimizer.param_groups]


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    grad_clip: float = 1.0,
) -> Dict[str, float]:
    """Train for one epoch."""
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []
    
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        
        if grad_clip > 0:
            nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        
        optimizer.step()
        
        total_loss += loss.item() * images.size(0)
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.cpu().numpy().tolist())
        all_labels.extend(labels.cpu().numpy().tolist())
    
    n = len(all_labels)
    return {
        "loss": total_loss / n,
        "accuracy": accuracy_score(all_labels, all_preds),
        "macro_f1": f1_score(all_labels, all_preds, average="macro", zero_division=0),
    }


@torch.no_grad()
def validate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> Dict[str, float]:
    """Validate the model."""
    model.eval()
    total_loss = 0.0
    all_preds, all_labels = [], []
    
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        total_loss += loss.item() * images.size(0)
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.cpu().numpy().tolist())
        all_labels.extend(labels.cpu().numpy().tolist())
    
    n = len(all_labels)
    return {
        "loss": total_loss / n,
        "accuracy": accuracy_score(all_labels, all_preds),
        "macro_f1": f1_score(all_labels, all_preds, average="macro", zero_division=0),
        "macro_precision": precision_score(all_labels, all_preds, average="macro", zero_division=0),
        "macro_recall": recall_score(all_labels, all_preds, average="macro", zero_division=0),
    }


def plot_training_curves(history: Dict[str, List], save_path: str, title: str = ""):
    """Generates training curve plots."""
    epochs = range(1, len(history["train_loss"]) + 1)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Loss
    axes[0].plot(epochs, history["train_loss"], "o-", color="#1f77b4", label="Train", linewidth=2, markersize=4)
    axes[0].plot(epochs, history["val_loss"], "s--", color="#ff7f0e", label="Val", linewidth=2, markersize=4)
    axes[0].set_title("Loss", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.4)
    
    # Accuracy
    axes[1].plot(epochs, [a * 100 for a in history["train_acc"]], "o-", color="#2ca02c", label="Train", linewidth=2, markersize=4)
    axes[1].plot(epochs, [a * 100 for a in history["val_acc"]], "s--", color="#d62728", label="Val", linewidth=2, markersize=4)
    axes[1].set_title("Accuracy (%)", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy (%)")
    axes[1].legend()
    axes[1].grid(True, linestyle="--", alpha=0.4)
    
    # Macro F1
    axes[2].plot(epochs, history["val_macro_f1"], "D-", color="#9467bd", label="Val Macro F1", linewidth=2, markersize=4)
    axes[2].set_title("Validation Macro F1", fontsize=13, fontweight="bold")
    axes[2].set_xlabel("Epoch")
    axes[2].set_ylabel("F1-Score")
    axes[2].legend()
    axes[2].grid(True, linestyle="--", alpha=0.4)
    
    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 25,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    warmup_epochs: int = 3,
    min_lr: float = 1e-6,
    label_smoothing: float = 0.05,
    use_focal_loss: bool = False,
    grad_clip: float = 1.0,
    patience: int = 10,
    checkpoint_dir: str = "checkpoints",
    results_dir: str = "results",
    experiment_name: str = "experiment",
    device: torch.device = None,
    class_weights: Optional[torch.Tensor] = None,
    seed: int = 42,
) -> Dict[str, Any]:
    """Full training pipeline with logging and checkpointing."""
    
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Set seed
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    model = model.to(device)
    
    # Loss function
    if use_focal_loss:
        criterion = FocalLoss(alpha=class_weights, gamma=2.0, label_smoothing=label_smoothing)
    else:
        criterion = nn.CrossEntropyLoss(
            weight=class_weights.to(device) if class_weights is not None else None,
            label_smoothing=label_smoothing
        )
    
    # Optimizer
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=lr, weight_decay=weight_decay)
    
    # Scheduler
    scheduler = CosineWarmupScheduler(optimizer, warmup_epochs, epochs, min_lr)
    
    # History tracking
    history = {
        "train_loss": [], "train_acc": [], "train_f1": [],
        "val_loss": [], "val_acc": [], "val_macro_f1": [],
        "val_macro_precision": [], "val_macro_recall": [],
        "lr": [], "epoch_time": [],
    }
    
    best_metric = 0.0
    best_epoch = 0
    patience_counter = 0
    
    checkpoint_path = os.path.join(checkpoint_dir, f"{experiment_name}_best.pth")
    
    print(f"\n{'='*70}")
    print(f" Training: {experiment_name}")
    print(f" Epochs: {epochs} | LR: {lr} | Device: {device} | Seed: {seed}")
    print(f" Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")
    print(f"{'='*70}\n")
    
    for epoch in range(1, epochs + 1):
        scheduler.step(epoch - 1)
        current_lr = scheduler.get_last_lr()[0]
        
        t0 = time.time()
        train_res = train_one_epoch(model, train_loader, optimizer, criterion, device, grad_clip)
        val_res = validate(model, val_loader, criterion, device)
        elapsed = time.time() - t0
        
        # Record history
        history["train_loss"].append(train_res["loss"])
        history["train_acc"].append(train_res["accuracy"])
        history["train_f1"].append(train_res["macro_f1"])
        history["val_loss"].append(val_res["loss"])
        history["val_acc"].append(val_res["accuracy"])
        history["val_macro_f1"].append(val_res["macro_f1"])
        history["val_macro_precision"].append(val_res["macro_precision"])
        history["val_macro_recall"].append(val_res["macro_recall"])
        history["lr"].append(current_lr)
        history["epoch_time"].append(elapsed)
        
        # Print progress
        print(
            f"Epoch [{epoch:02d}/{epochs:02d}] "
            f"Train Loss: {train_res['loss']:.4f} Acc: {train_res['accuracy']*100:.1f}% | "
            f"Val Loss: {val_res['loss']:.4f} Acc: {val_res['accuracy']*100:.1f}% F1: {val_res['macro_f1']:.4f} "
            f"({elapsed:.1f}s, lr: {current_lr:.6f})"
        )
        
        # Check for improvement (monitor val_macro_f1)
        current_metric = val_res["macro_f1"]
        if current_metric > best_metric:
            best_metric = current_metric
            best_epoch = epoch
            patience_counter = 0
            
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_accuracy": val_res["accuracy"],
                "val_macro_f1": val_res["macro_f1"],
                "experiment_name": experiment_name,
                "seed": seed,
            }, checkpoint_path)
            print(f"  -> Best checkpoint saved! Val F1: {best_metric:.4f}", flush=True)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"\n  Early stopping at epoch {epoch} (patience={patience})")
                break
    
    # Save training curves
    curves_path = os.path.join(results_dir, "training_curves.png")
    plot_training_curves(history, curves_path, title=experiment_name)
    
    # Save history
    history_path = os.path.join(results_dir, "training_history.json")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=4)
    
    total_time = sum(history["epoch_time"])
    print(f"\nTraining completed in {total_time:.1f}s ({total_time/60:.1f}min)")
    print(f"Best Val Macro F1: {best_metric:.4f} at epoch {best_epoch}")
    
    return {
        "best_epoch": best_epoch,
        "best_val_f1": best_metric,
        "best_val_acc": history["val_acc"][best_epoch - 1],
        "history": history,
        "checkpoint_path": checkpoint_path,
        "total_time_s": total_time,
    }
