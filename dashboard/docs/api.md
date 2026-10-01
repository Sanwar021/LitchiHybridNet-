# API Documentation: LitchiHybridNet FastAPI Backend

The FastAPI backend runs at `http://localhost:8000` with interactive Swagger docs at `/docs`.

## Base Endpoints

### 1. Overview & System
- `GET /api/overview` — High-level project KPIs, dataset totals, best model metrics, pipeline stepper
- `GET /api/system` — CPU, RAM, GPU, disk stats, PyTorch version, active Python process info
- `GET /api/progress` — Markdown content of `PROGRESS.md` and `FINAL_REPORT.md`

### 2. Dataset
- `GET /api/dataset/audit` — Audit summary (counts, duplicates, resolutions, splits)
- `GET /api/dataset/samples` — List of representative sample images per class
- `GET /api/dataset/duplicates` — Perceptual hash near-duplicate groups and statistics
- `GET /api/dataset/splits` — Train/Val/Test CSV split distribution and leakage verification
- `GET /api/dataset/frequency-analysis` — 2D FFT and PSD lesion frequency findings

### 3. Runs & Logs
- `GET /api/runs` — List of all executed experiment runs and aggregate stats
- `GET /api/runs/{run_id}` — Details, config, and epoch-by-epoch history for a specific run
- `GET /api/runs/{run_id}/stream` — Server-Sent Events (SSE) live epoch metrics stream
- `DELETE /api/runs/{run_id}` — Remove run artifacts

### 4. Job Control
- `POST /api/jobs/train` — Launch a training run subprocess with parameter overrides
- `POST /api/jobs/{type}` — Launch evaluate, robustness, explain, benchmark, or paper-build job
- `GET /api/jobs` — List queued, running, succeeded, and failed jobs
- `GET /api/jobs/{job_id}/logs/stream` — SSE stream of real-time stdout/stderr
- `POST /api/jobs/{job_id}/cancel` — Terminate a running subprocess

### 5. Results & Benchmarks
- `GET /api/results/comparison` — Main comparison benchmark across all evaluated models
- `GET /api/results/{run_id}/confusion` — Confusion matrix (normalized & raw counts)
- `GET /api/results/{run_id}/per-class` — Precision, recall, F1, support per class
- `GET /api/results/{run_id}/roc` — OvR ROC curves and AUC values
- `GET /api/results/{run_id}/calibration` — Expected Calibration Error (ECE) and reliability bins
- `GET /api/results/{run_id}/errors` — Gallery of misclassified validation/test instances

### 6. Ablations, Robustness, Efficiency, Stats
- `GET /api/ablations` — Multi-seed ablation matrix and groupings
- `GET /api/robustness` — Corruption suite degradation curves across 5 severities
- `GET /api/efficiency` — Params, FLOPs, model size, CPU latency, Pareto frontier
- `GET /api/stats/tests` — McNemar, paired bootstrap, Wilcoxon p-values

### 7. Explainability & Inference
- `GET /api/explain/gate-analysis` — Average SE-gate channel weights across classes
- `GET /api/explain/gabor-kernels` — 24 spatial filters (weights, frequencies, orientations)
- `POST /api/predict` — Multipart upload for live diagnosis, Grad-CAM heatmap, and Gabor features
- `POST /api/predict/robustness` — Apply image corruption and compare model responses live

### 8. Paper Assets & Export
- `GET /api/paper/figures` — List of high-res publication figures
- `GET /api/paper/tables` — Formatted LaTeX and CSV tables
- `GET /api/paper/pdf` — Stream or download compiled `main.pdf`
- `GET /api/paper/bib` — References in BibTeX format
- `GET /api/paper/checklist` — QA items status from `FINAL_REPORT.md`
- `POST /api/paper/build` — Trigger latexmk compiler
- `GET /api/export/bundle` — Zip download of submission package
