# Pre-Submission Scientific & Formatting Checklist — LitchiHybridNet

**Manuscript Title:** *LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection*  
**Date of Audit:** October 1, 2026  
**Auditor:** Scientific Editor & Integrity Verification Pipeline  

---

## 1. IEEEtran Formatting & Structure Compliance
- [x] **Document Class:** `\documentclass[journal]{IEEEtran}` with official `IEEEtran.cls` (v1.8b) bundled.
- [x] **Page Count & Layout:** Formatted as standard 2-column IEEE journal manuscript (~11--12 pages including tables, figures, and references).
- [x] **Title & Abstract:** Single paragraph, 215 words (within 150--250 word requirement), zero citations, zero mathematical equations.
- [x] **Index Terms:** 7 curated keywords: *Litchi leaf disease, learnable Gabor filters, texture fusion, field conditions, lightweight CNN, edge deployment, explainable AI*.
- [x] **Numbered Headings & Equations:** All sections numbered Roman (`I. Introduction` to `VIII. Conclusion`); all referenced mathematical equations numbered sequentially.
- [x] **Units & Notation:** Consistent SI units (`ms`, `MB`, `cycles/pixel`, `GHz`, `GFLOPs`); tensor dimensions strictly defined.

---

## 2. Empirical Integrity & Numerical Synchronization
- [x] **No Hardcoded Metrics in Text:** In-text numbers generated dynamically via `paper/auto_numbers.tex` using `scripts/make_auto_numbers.py`.
- [x] **`check_paper_numbers.py` Verification:** Passed with **0 errors**. Core Top-1 accuracy (99.04%), Macro-F1 (0.9904), test loss (0.0787), and dataset count (11,094) match ground truth files.
- [x] **Honest Negative Finding Reported:** Augmented dataset performance degradation (-1.10% accuracy, -0.0110 F1) documented and physically explained in Section VI-D.
- [x] **Exact Test Support:** All per-class precision, recall, and F1 values in Table 2 match `results/original/classification_report.csv` across all 1,665 test images.

---

## 3. Bibliographic Rigor & Citation Verification
- [x] **Total References:** 48 verified entries in `paper/references.bib`.
- [x] **`verify_references.py` Audit:** Passed with **0 errors**. Every reference possesses valid `title`, `author`, `year`, `journal`/`booktitle`, and verified DOI format.
- [x] **No Ghost References:** All citations in `paper/sections/*.tex` resolve to valid BibTeX keys; zero undefined citations.
- [x] **Literature Currency:** Spans foundational works (Daugman 1985, Manjunath 1996) up to recent high-impact 2021--2024 agricultural AI and vision architectures (ConvNeXt, Swin-T, MobileNetV3).

---

## 4. Figures and Visual Assets
- [x] **Resolution:** All 15 figures rendered at **300 DPI** using `scripts/make_paper_figures.py`.
- [x] **Color Palette:** Colorblind-friendly palettes (viridis, tab10, seaborn colorblind); consistent model color mapping across charts.
- [x] **Figure Sizing:** Single-column (3.5 in) and double-column (7.16 in) widths with legible typography (8--10 pt).
- [x] **Graphical Abstract:** Exported at 300 DPI to `paper/submission/graphical_abstract.png`.

---

## 5. Ethical, Reproducibility & Open Science Declarations
- [x] **Code Availability:** Complete PyTorch implementation, scripts, and pre-trained weights linked to GitHub (`https://github.com/Sanwar021/LitchiHybridNet-.git`).
- [x] **Data Availability:** BDLitchi public source explicitly cited; group-aware split manifests provided in `data/splits/`.
- [x] **Author Contributions:** Detailed CRediT statement provided in Section VIII.
- [x] **Conflict of Interest:** Explicit declaration of no competing financial or non-financial interests.
- [x] **Reproducibility Protocol:** Fixed random seeds (42, 123, 456, 789, 999), deterministic cuDNN flags, and hardware specifications documented in Section V.
