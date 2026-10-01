"""
Comprehensive evaluation for LitchiHybridNet.

Metrics:
- Accuracy, Balanced Accuracy, MCC, Cohen's Kappa
- Macro/Weighted Precision, Recall, F1
- ROC-AUC (OvR)
- Per-class metrics
- Confusion matrix (raw + normalized)
- ECE (Expected Calibration Error)
- Classification report (CSV + JSON)
"""

import os
import json
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, balanced_accuracy_score,
    f1_score, precision_score, recall_score,
    matthews_corrcoef, cohen_kappa_score,
    roc_auc_score, roc_curve, auc,
)


def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """Expected Calibration Error."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels).astype(float)
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        if mask.sum() > 0:
            bin_acc = accuracies[mask].mean()
            bin_conf = confidences[mask].mean()
            ece += mask.sum() / len(labels) * abs(bin_acc - bin_conf)
    return ece


def plot_confusion_matrix(cm, class_names, save_path, title="", normalize=True):
    """Saves a publication-quality confusion matrix plot."""
    if normalize:
        cm_plot = cm.astype("float") / (cm.sum(axis=1)[:, np.newaxis] + 1e-9)
        fmt = ".1%"
    else:
        cm_plot = cm
        fmt = "d"
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm_plot, annot=True, fmt=fmt, cmap="Blues",
        xticklabels=class_names, yticklabels=class_names,
        cbar=True, annot_kws={"size": 9}, linewidths=0.5,
    )
    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Class", fontsize=12, fontweight="bold")
    plt.ylabel("True Class", fontsize=12, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_roc_curves(all_labels, all_probs, class_names, save_path):
    """Plot per-class ROC curves."""
    n_classes = len(class_names)
    labels_onehot = np.eye(n_classes)[all_labels]
    probs_arr = np.array(all_probs)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab20(np.linspace(0, 1, n_classes))
    
    for i, (cls, color) in enumerate(zip(class_names, colors)):
        fpr, tpr, _ = roc_curve(labels_onehot[:, i], probs_arr[:, i])
        roc_auc_val = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=color, lw=1.5, label=f"{cls} (AUC={roc_auc_val:.3f})")
    
    ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5)
    ax.set_xlabel("False Positive Rate", fontsize=12, fontweight="bold")
    ax.set_ylabel("True Positive Rate", fontsize=12, fontweight="bold")
    ax.set_title("ROC Curves (One-vs-Rest)", fontsize=14, fontweight="bold")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_reliability_diagram(probs, labels, save_path, n_bins=15):
    """Reliability diagram for calibration assessment."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels).astype(float)
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_accs, bin_confs, bin_counts = [], [], []
    
    for i in range(n_bins):
        mask = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        if mask.sum() > 0:
            bin_accs.append(accuracies[mask].mean())
            bin_confs.append(confidences[mask].mean())
            bin_counts.append(mask.sum())
        else:
            bin_accs.append(0)
            bin_confs.append((bin_boundaries[i] + bin_boundaries[i + 1]) / 2)
            bin_counts.append(0)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={"height_ratios": [3, 1]})
    
    ax1.bar(bin_confs, bin_accs, width=1/n_bins * 0.8, alpha=0.7, color="#2196F3", edgecolor="black")
    ax1.plot([0, 1], [0, 1], "r--", lw=2, label="Perfect calibration")
    ax1.set_ylabel("Accuracy", fontsize=12, fontweight="bold")
    ax1.set_title("Reliability Diagram", fontsize=14, fontweight="bold")
    ax1.legend()
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.grid(True, linestyle="--", alpha=0.3)
    
    ax2.bar(bin_confs, bin_counts, width=1/n_bins * 0.8, alpha=0.7, color="#FF9800", edgecolor="black")
    ax2.set_xlabel("Confidence", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Count", fontsize=12, fontweight="bold")
    ax2.set_xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    test_loader: DataLoader,
    class_names: List[str],
    device: torch.device,
    save_dir: str,
    dataset_name: str = "BDLitchi",
) -> Dict[str, Any]:
    """
    Comprehensive model evaluation with all metrics and visualizations.
    """
    os.makedirs(save_dir, exist_ok=True)
    model.eval()
    
    all_preds, all_labels, all_probs = [], [], []
    
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        
        outputs = model(images)
        probs = torch.softmax(outputs, dim=1)
        preds = torch.argmax(probs, dim=1)
        
        all_preds.extend(preds.cpu().numpy().tolist())
        all_labels.extend(labels.cpu().numpy().tolist())
        all_probs.extend(probs.cpu().numpy().tolist())
    
    all_labels = np.array(all_labels)
    all_preds = np.array(all_preds)
    all_probs = np.array(all_probs)
    
    # ─── Compute all metrics ────────────────────────────────────────
    n_classes = len(class_names)
    labels_onehot = np.eye(n_classes)[all_labels]
    
    metrics = {
        "dataset_name": dataset_name,
        "total_test_samples": len(all_labels),
        "accuracy": float(accuracy_score(all_labels, all_preds)),
        "balanced_accuracy": float(balanced_accuracy_score(all_labels, all_preds)),
        "macro_precision": float(precision_score(all_labels, all_preds, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(all_labels, all_preds, average="macro", zero_division=0)),
        "macro_f1": float(f1_score(all_labels, all_preds, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(all_labels, all_preds, average="weighted", zero_division=0)),
        "weighted_precision": float(precision_score(all_labels, all_preds, average="weighted", zero_division=0)),
        "weighted_recall": float(recall_score(all_labels, all_preds, average="weighted", zero_division=0)),
        "mcc": float(matthews_corrcoef(all_labels, all_preds)),
        "cohen_kappa": float(cohen_kappa_score(all_labels, all_preds)),
        "ece": float(compute_ece(all_probs, all_labels)),
    }
    
    # ROC-AUC
    try:
        metrics["roc_auc_macro"] = float(roc_auc_score(labels_onehot, all_probs, average="macro", multi_class="ovr"))
        metrics["roc_auc_weighted"] = float(roc_auc_score(labels_onehot, all_probs, average="weighted", multi_class="ovr"))
    except Exception:
        metrics["roc_auc_macro"] = None
        metrics["roc_auc_weighted"] = None
    
    # Per-class report
    report = classification_report(
        all_labels, all_preds, target_names=class_names,
        output_dict=True, zero_division=0
    )
    metrics["classification_report"] = report
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    metrics["confusion_matrix"] = cm.tolist()
    
    # ─── Save plots ────────────────────────────────────────────────
    plot_confusion_matrix(
        cm, class_names,
        os.path.join(save_dir, "confusion_matrix.png"),
        title=f"Confusion Matrix — {dataset_name}\n(Accuracy: {metrics['accuracy']*100:.2f}%)",
    )
    
    plot_roc_curves(
        all_labels, all_probs, class_names,
        os.path.join(save_dir, "roc_curves.png"),
    )
    
    plot_reliability_diagram(
        all_probs, all_labels,
        os.path.join(save_dir, "reliability_diagram.png"),
    )
    
    # Save CSV report
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv(os.path.join(save_dir, "classification_report.csv"))
    
    # Save metrics JSON
    # Round numeric values
    metrics_rounded = {}
    for k, v in metrics.items():
        if isinstance(v, float):
            metrics_rounded[k] = round(v, 4)
        else:
            metrics_rounded[k] = v
    
    with open(os.path.join(save_dir, "metrics.json"), "w") as f:
        json.dump(metrics_rounded, f, indent=4)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f" Evaluation Results: {dataset_name}")
    print(f"{'='*50}")
    print(f"  Accuracy:          {metrics['accuracy']*100:.2f}%")
    print(f"  Balanced Accuracy: {metrics['balanced_accuracy']*100:.2f}%")
    print(f"  Macro F1:          {metrics['macro_f1']:.4f}")
    print(f"  Weighted F1:       {metrics['weighted_f1']:.4f}")
    print(f"  MCC:               {metrics['mcc']:.4f}")
    print(f"  Cohen's Kappa:     {metrics['cohen_kappa']:.4f}")
    print(f"  ECE:               {metrics['ece']:.4f}")
    if metrics["roc_auc_macro"]:
        print(f"  ROC-AUC (macro):   {metrics['roc_auc_macro']:.4f}")
    print(f"{'='*50}\n")
    
    return metrics
