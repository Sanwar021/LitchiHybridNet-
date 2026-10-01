# Data Contract: LitchiHybridNet Dashboard & Pipeline

This document defines the schema, types, and on-disk expectations for every file produced by the ML pipeline and consumed by the FastAPI backend and React frontend.

---

## 1. Dataset Audit (`data/audit/dataset_audit.json`)

```json
{
  "total_images": 11094,
  "num_classes": 11,
  "classes": ["Black Spot", "Burned Leaf", ...],
  "class_distribution": {
    "Black Spot": 1120,
    "Burned Leaf": 1050
  },
  "resolution_stats": {
    "min_width": 224,
    "max_width": 4032,
    "min_height": 224,
    "max_height": 3024,
    "mean_width": 1280.5,
    "mean_height": 960.2
  },
  "duplicates": {
    "exact_hash_duplicates": 202,
    "near_duplicate_groups": 924,
    "cross_class_duplicates": 0
  },
  "splits": {
    "train": 7729,
    "val": 1691,
    "test": 1674,
    "group_aware": true,
    "leakage_count": 0
  }
}
```

---

## 2. Per-Run Training History (`experiments/results/{run_id}/training_history.json`)

```json
{
  "train_loss": [0.654, 0.432, 0.289],
  "train_acc": [0.781, 0.865, 0.912],
  "train_f1": [0.775, 0.860, 0.910],
  "val_loss": [0.580, 0.395, 0.250],
  "val_acc": [0.812, 0.884, 0.935],
  "val_macro_f1": [0.808, 0.880, 0.932],
  "val_macro_precision": [0.815, 0.885, 0.936],
  "val_macro_recall": [0.805, 0.878, 0.930],
  "lr": [0.00033, 0.00066, 0.00100],
  "epoch_time": [124.5, 122.1, 123.8]
}
```

---

## 3. Per-Run Final Experiment Result (`experiments/results/{run_id}/experiment_result.json`)

```json
{
  "experiment_name": "hybrid_seed42",
  "model_type": "hybrid",
  "seed": 42,
  "total_params": 5572184,
  "trainable_params": 5572184,
  "train_results": {
    "best_epoch": 24,
    "best_val_f1": 0.9904,
    "total_time_s": 3050.2
  },
  "test_metrics": {
    "accuracy": 0.9904,
    "balanced_accuracy": 0.9902,
    "macro_f1": 0.9904,
    "weighted_f1": 0.9903,
    "macro_precision": 0.9902,
    "macro_recall": 0.9908,
    "mcc": 0.9894,
    "cohen_kappa": 0.9894,
    "ece": 0.0124
  }
}
```

---

## 4. Multi-Seed Aggregated Result (`experiments/results/{model_name}_aggregated.json`)

```json
{
  "model_type": "hybrid",
  "num_seeds": 5,
  "accuracy_mean": 0.9904,
  "accuracy_std": 0.0012,
  "macro_f1_mean": 0.9904,
  "macro_f1_std": 0.0011,
  "balanced_accuracy_mean": 0.9902,
  "balanced_accuracy_std": 0.0013,
  "mcc_mean": 0.9894,
  "mcc_std": 0.0014,
  "avg_training_time_s": 3020.5
}
```

---

## 5. Main Comparison Table (`tables/main_comparison.csv`)

| model | backbone | params_m | flops_m | accuracy_mean | accuracy_std | macro_f1_mean | macro_f1_std | mcc_mean | latency_cpu_ms | size_mb |
|-------|----------|----------|---------|---------------|--------------|---------------|--------------|----------|----------------|---------|
| LitchiHybridNet | MobileNetV3-Large + Gabor | 5.57 | 235.0 | 99.04 | 0.12 | 0.9904 | 0.0010 | 0.989 | 38.4 | 21.25 |
| MobileNetV3-Large | MobileNetV3-Large | 5.40 | 219.0 | 96.82 | 0.35 | 0.9675 | 0.0030 | 0.965 | 32.1 | 20.60 |
| EfficientNet-B0 | EfficientNet-B0 | 5.30 | 390.0 | 97.15 | 0.28 | 0.9710 | 0.0020 | 0.968 | 52.0 | 20.20 |

---

## 6. Ablation Studies (`tables/ablation_study.csv`)

```csv
ablation_group,variant,params_m,accuracy_mean,accuracy_std,macro_f1_mean,macro_f1_std
branch,Gabor Texture Only,0.26,86.80,0.45,0.8640,0.0050
branch,CNN Backbone Only (MobileNetV3),5.40,96.82,0.35,0.9675,0.0030
branch,Fixed Gabor + CNN (Concat),5.57,97.52,0.28,0.9745,0.0025
branch,Learnable Gabor + CNN (Concat),5.57,98.22,0.22,0.9815,0.0020
branch,LitchiHybridNet (Learnable + Gated),5.57,99.04,0.12,0.9904,0.0010
fusion,Simple Addition,5.55,97.10,0.30,0.9710,0.0028
fusion,Channel Concatenation,5.57,98.22,0.22,0.9815,0.0020
fusion,Cross-Attention,5.75,98.70,0.18,0.9870,0.0016
fusion,SE-Gated Fusion (Proposed),5.57,99.04,0.12,0.9904,0.0010
```

---

## 7. Robustness Corruption Suite (`tables/robustness_mca.csv`)

```csv
corruption,severity,litchi_hybridnet,mobilenetv3,efficientnet_b0,resnet50
motion_blur,1,98.5,95.4,95.8,96.1
motion_blur,2,97.8,93.1,93.9,94.5
motion_blur,3,96.4,89.6,90.4,91.8
motion_blur,4,94.2,84.8,86.0,87.2
motion_blur,5,91.8,79.2,80.5,82.0
gaussian_noise,1,98.7,95.8,96.2,96.5
...
```

---

## 8. Efficiency & Deployment (`tables/efficiency.csv`)

```csv
model_variant,format,device,batch_size,params_m,flops_m,size_mb,latency_mean_ms,latency_p95_ms,accuracy
LitchiHybridNet_FP32,PyTorch,CPU,1,5.57,235.0,21.25,38.4,42.1,99.04
LitchiHybridNet_ONNX,ONNX,CPU,1,5.57,235.0,21.18,26.2,29.5,99.04
LitchiHybridNet_INT8,ONNX_INT8,CPU,1,5.57,235.0,5.40,14.8,17.2,98.72
```

---

## 9. Statistical Tests (`tables/stats_tests.json`)

```json
{
  "comparison": "LitchiHybridNet vs MobileNetV3-Large",
  "mcnemar": {
    "statistic": 34.28,
    "p_value": 4.77e-9,
    "significant": true
  },
  "wilcoxon": {
    "statistic": 0.0,
    "p_value": 0.00098,
    "significant": true
  },
  "paired_bootstrap_95ci": {
    "lower": 0.0184,
    "upper": 0.0261,
    "mean_diff": 0.0222
  }
}
```

---

## 10. Live Inference Output Schema (`POST /api/predict`)

```json
{
  "model_id": "hybrid_seed42",
  "predicted_class": "Leaf Blight Disease",
  "predicted_index": 6,
  "confidence": 0.9942,
  "probabilities": {
    "Black Spot": 0.0001,
    "Leaf Blight Disease": 0.9942,
    "Healthy Leaf": 0.0002
  },
  "inference_time_ms": 38.2,
  "gradcam_base64": "data:image/png;base64,...",
  "gabor_response_base64": "data:image/png;base64,...",
  "gate_values": {
    "cnn_gate_mean": 0.58,
    "gabor_gate_mean": 0.42
  }
}
```
