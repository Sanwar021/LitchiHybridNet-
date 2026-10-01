# Journal Target Shortlist & Submission Guide — LitchiHybridNet

This document outlines the top 5 realistic, high-impact Q1/Q2 journal venues for submitting the **LitchiHybridNet** manuscript, along with their scope, impact factors, indexing quartiles, formatting requirements, and conversion commands.

---

## 1. Top Target Venues Summary Table

| Venue | Publisher | 2024–2026 Impact Factor | JCR Quartile | Typical Review Speed | Primary Focus Alignment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Computers and Electronics in Agriculture (COMPAG)** | Elsevier | **10.3** | **Q1** (Top 1%) | 6–10 weeks | **Optimal Match**: Demands novel AI/CV architectures solving real field-condition crop production problems. |
| **IEEE Transactions on AgriFood Electronics (TAFE)** | IEEE | Emerging / Indexed | **Q1 / High CASS** | 8–12 weeks | **Optimal IEEE Match**: Edge hardware deployment, lightweight neural models, IoT sensor integration. |
| **Smart Agricultural Technology (SAT)** | Elsevier | **6.4** | **Q1** | 5–8 weeks | High-speed companion to COMPAG, focusing on field-deployable technologies and embedded software. |
| **Precision Agriculture** | Springer Nature | **5.4** | **Q1** | 8–12 weeks | In-field variable-rate applications, robotic scouting, foliar pathology quantification. |
| **IEEE Access** | IEEE | **3.9** | **Q1 / Q2** | 4–6 weeks (Fast track) | Open access multidisciplinary IEEE journal; directly accepts `IEEEtran.cls` without reformatting. |

---

## 2. In-Depth Journal Profiles

### Target 1: *Computers and Electronics in Agriculture* (Elsevier)
- **Aims & Scope:** Publishes original research presenting novel algorithms, hardware, and electronic instrumentation applied to agriculture, agronomy, and horticulture. Explicitly demands technical innovation in machine vision and AI beyond off-the-shelf transfer learning.
- **Why LitchiHybridNet Fits:** 
  1. The learnable Gabor layer provides mathematical architectural novelty.
  2. The $dHash$ benchmark audit addresses a critical flaw in prior agricultural datasets.
  3. Real-world robustness evaluations and negative findings on augmentation offer high scientific value.
- **Submission Requirements:** Single or double-column PDF, structured abstract (150–250 words), 3–5 highlights ($\le 85$ characters each), graphical abstract (required).
- **Template:** Uses `elsarticle.cls` (`\documentclass[preprint,12pt]{elsarticle}`).

---

### Target 2: *IEEE Transactions on AgriFood Electronics* (IEEE TAFE)
- **Aims & Scope:** Sponsored by the IEEE Circuits and Systems Society (CASS). Covers smart agriculture, electronics, embedded microcomputing, sensory hardware, and AI at the agricultural edge.
- **Why LitchiHybridNet Fits:** 
  1. Detailed physical profiling on Raspberry Pi 4 Model B and NVIDIA Jetson Nano.
  2. Post-training INT8 dynamic quantization achieving 34.2 ms (~29 FPS) execution.
  3. Direct adherence to IEEE publication style and double-column LaTeX layout.
- **Template:** Directly uses the compiled `IEEEtran.cls` in this repository!

---

### Target 3: *Smart Agricultural Technology* (Elsevier)
- **Aims & Scope:** Dedicated to practical, field-validated technological solutions in precision agriculture, mobile smart systems, and IoT deployment.
- **Why LitchiHybridNet Fits:** Practical focus on rural smallholder orchards, low-cost microcomputer execution, and eliminating chemical fungicide spraying.

---

### Target 4: *Precision Agriculture* (Springer)
- **Aims & Scope:** Emphasizes spatial and temporal variability management, robotic spraying, sensor technologies, and canopy disease monitoring.
- **Template:** Uses `sn-jnl.cls` (Springer Nature LaTeX author template).

---

## 3. Template Switching Guide

The primary manuscript in this repository is built in native **IEEE journal format** (`IEEEtran.cls`). If submitting to **Elsevier (COMPAG / SAT)**, follow these simple adaptation steps:

### A. Automatic Conversion to Elsevier `elsarticle`
To convert `main.tex` for Elsevier:
1. Replace `\documentclass[journal]{IEEEtran}` with:
   ```latex
   \documentclass[preprint,12pt,authoryear]{elsarticle}
   \usepackage{amsmath,amsfonts,amssymb,graphicx,booktabs,multirow,url}
   \input{auto_numbers.tex}
   ```
2. Replace `\maketitle` and IEEE author blocks with Elsevier frontmatter:
   ```latex
   \begin{frontmatter}
   \title{LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection}
   \author[buet]{M. Tariqul Islam\corref{cor1}}
   \ead{tariqul@cse.buet.ac.bd}
   \author[buet]{M. A. Rahman}
   \author[bari]{Nadia Akter}
   \author[bari]{P. K. Roy}
   \cortext[cor1]{Corresponding author}
   \address[buet]{Department of Computer Science and Engineering, BUET, Dhaka 1205, Bangladesh}
   \address[bari]{Plant Pathology Division, BARI, Gazipur 1701, Bangladesh}
   \begin{abstract}
   ...
   \end{abstract}
   \begin{highlights}
   \input{submission/highlights.txt}
   \end{highlights}
   \begin{keyword}
   Litchi leaf disease \sep Learnable Gabor filters \sep Texture fusion \sep Edge deployment
   \end{keyword}
   \end{frontmatter}
   ```
3. Keep all `\input{sections/...}` and `\input{tables/...}` exactly identical!

---

## 4. Final Submission Checklist
Before uploading to the submission portal (e.g. Editorial Manager or ScholarOne):
1. **Manuscript PDF:** `paper/main.pdf`
2. **Graphical Abstract:** `paper/submission/graphical_abstract.png`
3. **Highlights:** `paper/submission/highlights.txt`
4. **Cover Letter:** `paper/submission/cover_letter.md`
5. **Supplementary Information:** `paper/supplementary/supplementary.tex`
6. **Code & Data URL:** `https://github.com/Sanwar021/LitchiHybridNet-.git`
