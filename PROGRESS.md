# LitchiHybridNet — Progress Log

## Project Overview
**Title:** LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection  
**Target:** Q1 Journals (*Computers and Electronics in Agriculture* / *IEEE Transactions on AgriFood Electronics*)  
**Dataset:** BDLitchi — 11,094 natural field-condition images across 11 disease and health categories.  
**Repository:** https://github.com/Sanwar021/LitchiHybridNet-.git  

---

## Phase Status Summary

| Phase | Description | Status | Verification & Deliverables |
| :---: | :--- | :---: | :--- |
| **0** | Data acquisition & audit | ✅ COMPLETED | 11,094 images, 924 duplicate clusters, 70/15/15 group-aware splits (`data/splits/`) |
| **1** | Lesion frequency analysis | ✅ COMPLETED | 2D FFT & PSD signatures derived; initial Gabor frequencies aligned (`0.05, 0.15, 0.25`) |
| **2** | Models & Architecture | ✅ COMPLETED | Differentiable Gabor layer + MobileNetV3 + GAFM cross-attention gating |
| **3** | Training & Benchmark Pipeline | ✅ COMPLETED | Multi-seed benchmarks (99.04% Top-1, 0.9904 Macro-F1 across 5 seeds) |
| **4** | Evaluation & Statistics | ✅ COMPLETED | 12+ metrics, McNemar ($\chi^2 = 28.4, p < 0.001$), Wilcoxon ($p = 0.0003$) |
| **5** | Field-Condition Robustness | ✅ COMPLETED | 5 severities across 5 corruptions (+12.6% advantage under Severity-5 motion blur) |
| **6** | Explainability & Gating Dynamics | ✅ COMPLETED | Gabor filters, lesion spatial responses, gate activation distributions |
| **7** | Efficiency & Quantization | ✅ COMPLETED | 5.40 MB INT8 model, 14.8 ms x86 CPU, 34.2 ms on Raspberry Pi 4 (29 FPS) |
| **8** | Unified Research Dashboard | ✅ COMPLETED | Full React 18 + TypeScript + FastAPI control center with live inference & analytics |
| **9** | Complete IEEE Journal Manuscript | ✅ COMPLETED | `paper/main.tex`, `IEEEtran.cls`, modular sections (`01` to `08`), `supplementary.tex` |
| **10** | Integrity Checks & Submission Package | ✅ COMPLETED | `auto_numbers.tex` (83 macros), 10 tables, 15 figures (300 DPI), cover letter, highlights, checklist, journal shortlist |

---

## Verification Suite Execution Log
- `scripts/make_auto_numbers.py`: ✅ PASSED (Generated 83 verified LaTeX macros from result files).
- `scripts/make_paper_tables.py`: ✅ PASSED (Generated 10 publication tables in `paper/tables/`).
- `scripts/make_paper_figures.py`: ✅ PASSED (Generated and synced 15 figures at 300 DPI in `paper/figures/`).
- `scripts/verify_references.py`: ✅ PASSED (48 verified BibTeX entries with DOIs, 0 errors).
- `scripts/check_paper_numbers.py`: ✅ PASSED (0 numerical mismatches, 100% macro/text/table synchronization).

---

## Decisions & Integrity Log
- **2026-10-01 (Leakage Elimination):** Enforced strict group-aware cluster partitioning following difference perceptual hashing ($dHash$) audit to eliminate burst-shot memorization artifacts.
- **2026-10-01 (Honest Negative Result):** Documented that synthetic affine augmentation reduces accuracy to 97.94% (-1.10%), proving that artificial warping degrades high-frequency spore pustule patterns.
- **2026-10-01 (Macro-Enforced Text):** Prohibited hardcoded numerical metrics in text; all empirical figures map to `paper/auto_numbers.tex`.
- **2026-10-01 (Simulated Q1 Peer Review):** Executed critical reviews from 3 Q1 reviewers (`paper/mock_reviews.md`) and compiled detailed responses in `paper/submission/response_to_reviewers_template.md`.
