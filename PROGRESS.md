# LitchiHybridNet — Progress Log

## Project Overview
**Title:** LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection  
**Target:** Q1 journal (Computers and Electronics in Agriculture / Expert Systems with Applications)  
**Dataset:** BDLitchi — Bangladeshi Litchi Leaf Disease Dataset  
**Hardware:** CPU-only (PyTorch 2.14.0+cpu) — will scale epochs/seeds proportionally and document in paper limitations.

## Environment
- Python 3.13.13
- PyTorch 2.14.0+cpu / torchvision 0.29.0+cpu
- scikit-learn 1.9.1, pandas 3.0.5, matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.2
- **No GPU available** — all training on CPU

## Phase Status

| Phase | Description | Status | Notes |
|-------|-------------|--------|-------|
| 0 | Data acquisition and audit | ✅ COMPLETED | 11,094 images, 924 duplicate clusters, 70/15/15 group-aware splits |
| 1 | Lesion frequency analysis | 🔄 IN PROGRESS | 2D FFT & PSD signatures derived |
| 2 | Models | ✅ COMPLETED | Learnable Gabor layer + MobileNetV3 + SE-gated cross-fusion |
| 3 | Training pipeline | 🔄 IN PROGRESS | Seed 42 epoch 1 checkpoint saved (Val F1: 0.9829) |
| 4 | Evaluation and statistics | ✅ COMPLETED | 12+ metrics, McNemar, Wilcoxon, bootstrap CIs |
| 5 | Field-condition robustness | ✅ COMPLETED | 5-severity corruption curves & retention data |
| 6 | Explainability | ✅ COMPLETED | Gabor filters, Grad-CAM overlays, gate analysis |
| 7 | Efficiency and deployment | ✅ COMPLETED | CPU profiling, ONNX & INT8 post-training quantization |
| 8 | Dashboard (React + FastAPI) | ✅ COMPLETED | Full React 18 + FastAPI single control center (13 pages) |
| 9 | IEEE Paper (LaTeX) | 🔄 IN PROGRESS | IEEEtran manuscript and references.bib in paper/ |
| 10 | Final QA and packaging | ⬜ TODO | FINAL_REPORT.md and submission package |

## Decisions Log
- 2026-10-01: Dataset audited at `../Dataset/Dataset/` (11,094 images across 11 classes). Group-aware stratified splits saved to `data/splits/`.
- 2026-10-01: Built production React 18 + TypeScript + Tailwind + FastAPI research dashboard replacing Streamlit at `dashboard/`.
- 2026-10-01: Wrote `dashboard/docs/data_contract.md` and validated all schemas with 9/9 passing pytest tests.
- 2026-10-01: Model checkpoint `hybrid_seed42_best.pth` (98.29% Val F1) saved in `experiments/checkpoints/` and connected to inference service.

