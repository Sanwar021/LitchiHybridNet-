# LitchiHybridNet React + FastAPI Research Dashboard

Production-grade, publication-connected research dashboard and clinical diagnosis studio for **LitchiHybridNet**.

---

## Architecture Overview

```
dashboard/
  backend/
    app/
      main.py          # FastAPI entrypoint, mounts API & React bundle
      core/            # Config, SQLite engine, Lifespan
      models/          # SQLAlchemy Job and Run models
      schemas/         # Pydantic v2 data contracts
      services/        # Inference, JobManager, RunRegistry, Robustness, StreamService
      routers/         # 13 REST & SSE routers
    tests/             # Pytest test suite (100% pass)
  frontend/
    src/
      pages/           # 13 comprehensive research pages
      components/      # Navigation, Header, Glassmorphism Cards
      services/        # Typed API client
      types/           # TypeScript interfaces matching OpenAPI
  docs/
    data_contract.md   # Zero-leakage data contract & schema specification
    api.md             # REST & SSE endpoint documentation
```

---

## 13 Fully Integrated Pages

1. **Overview**: Headline KPIs (99.04% Acc, 0.9904 Macro-F1, 14.8 ms CPU Latency), pipeline stepper (Phases 0–10).
2. **Dataset & Audit**: 11,094 images, 924 near-duplicate groups, zero-leakage group-aware 70/15/15 partition verification.
3. **Training Studio**: Interactive parameter configuration form, launch button, SSE stdout/stderr live console.
4. **Runs & Compare**: Registry of all runs across seeds, duration, best validation F1, checkpoint verification.
5. **Results & Baselines**: Full benchmark table comparing LitchiHybridNet with 8 baselines, statistical significance (McNemar, Wilcoxon, paired bootstrap), per-class precision/recall.
6. **Ablations**: Grouped analysis of dual-branch fusion, learnable Gabor parameters, and filter bank scales.
7. **Robustness Suite**: 5-severity degradation curves under blur, noise, solar glare, and clutter.
8. **Explainability**: 24-channel Gabor kernel specifications and SE-gate channel distributions across 11 disease classes.
9. **Inference Lab**: Drag-and-drop field leaf diagnostic testing, probability distribution, and Grad-CAM heatmap overlays.
10. **Efficiency & Edge**: CPU profiling, Pareto frontier, ONNX INT8 post-training quantization (2.6× speedup, 74.5% size reduction).
11. **Paper Assets**: High-resolution figures (300+ DPI), formatted LaTeX tables, verified BibTeX, and QA checklist.
12. **Jobs & Logs**: Active and historical background processes with status, PID, and cancel controls.
13. **System & Config**: Real-time CPU, RAM, disk utilization, PyTorch version, and Git commit tracking.

---

## Quickstart

### 1. Launch Unified Server (FastAPI + React)
```bash
make dashboard
# or
python -m uvicorn dashboard.backend.app.main:app --host 0.0.0.0 --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** for the React Dashboard.  
Open **[http://localhost:8000/docs](http://localhost:8000/docs)** for interactive Swagger OpenAPI documentation.

### 2. Launch Vite Dev Mode (with Hot Reloading)
```bash
make dashboard-dev
# or
cd dashboard/frontend && npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)**.

### 3. Run Backend API Tests
```bash
make dashboard-test
# or
python -m pytest dashboard/backend/tests/test_api.py -v
```
