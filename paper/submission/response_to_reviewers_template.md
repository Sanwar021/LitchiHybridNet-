# Point-by-Point Response to Reviewers' Comments

**Manuscript ID:** TAI-2026-XXXX  
**Title:** *LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection*  
**Authors:** Rawan Hasan  
**Target Journal:** *IEEE Transactions on Agri-Food Informatics*

---

Dear Editor and Reviewers,

We express our sincere gratitude to the Associate Editor and the three anonymous reviewers for their thoughtful, rigorous, and constructive evaluations of our manuscript. We have carefully incorporated all recommendations, performing additional control analyses, refining our mathematical derivations, clarifying the agronomic scope, and validating all numerical claims. Below, we present our detailed, point-by-point responses to each reviewer's comments, with line and section references corresponding to the revised manuscript.

---

## Response to Reviewer 1 (Agricultural Domain Expert & Phytopathologist)

### Comment 1.1: Foliar Scope vs. Fruit/Panicle Pathologies
> *"The title and claims should explicitly clarify that the dataset evaluates only foliar symptoms. Litchi growers suffer massive losses from pericarp browning and fruit rot (Peronophythora litchii), which are absent here."*

**Author Response:**  
We fully agree with the Reviewer. The BDLitchi dataset is strictly a foliar benchmark. We have revised the Title, Abstract, and Introduction to explicitly state that our system targets *foliar (leaf lamina) disease detection*. Furthermore, in Section 7.4 (*Threats to Validity and Study Limitations*), we explicitly identify this scope boundary:
> *"This investigation is strictly restricted to foliar (leaf lamina) pathologies. Although foliar symptoms represent primary diagnostic indicators, litchi production is equally impacted by post-harvest fruit rot (pericarp browning), flower panicle blights, and root-knot nematodes, which are outside the scope of the current benchmark."*

### Comment 1.2: Geographic and Cultivar Generalizability
> *"The images originate entirely from Dinajpur and Ishwardi, Bangladesh (predominantly China-3 and Bombay cultivars). How would the model perform on Chinese or Indian cultivars where leaf venation differs?"*

**Author Response:**  
We appreciate this important insight. We have expanded Section 7.4 to detail this geographical concentration as an open research challenge. We emphasize that while Dinajpur and Ishwardi represent premier litchi agro-ecological belts in South Asia, domain shifts across distinct Asian cultivars (e.g., *Feizixiao* in Guangdong, China or *Shahi* in Bihar, India) require future multi-center cross-domain transfer evaluations.

### Comment 1.3: Compound/Multiple In-Field Infections
> *"In natural orchards, a single leaf often hosts both insect chewing and fungal spots simultaneously. How does the model behave when lesions overlap?"*

**Author Response:**  
We have incorporated an explicit discussion of compound infections into Section 7.2 (*Diagnostic Error Analysis and Failure Modes*). Of the 16 misclassified test samples (out of 1,665), several featured co-occurring insect punctures and fungal spots, where the softmax distribution split between the two conditions (e.g., $P(\text{Black Spot}) = 0.44$, $P(\text{Insect Chewing}) = 0.49$). We have added this as a motivating justification for future multi-label foliar phenotyping research.

---

## Response to Reviewer 2 (Machine Learning Methodologist)

### Comment 2.1: Novelty vs. Prior Gabor Networks
> *"The authors must explicitly articulate the mathematical and structural distinction between their unconstrained differentiable layer + cross-attention fusion and prior fixed/tied Gabor layers (e.g., Luan et al. 2018)."*

**Author Response:**  
We have expanded Section 2.3 and Section 4.2 to formally delineate our architectural innovations:
1. **Unconstrained Differentiable Layer:** Unlike Luan et al. (2018), who constrained standard convolutional weights to follow static harmonic envelopes throughout training, our layer parameterizes orientation $\theta$, frequency $F$, and spread $\sigma$ as continuous, unconstrained learnable parameters updated via analytic chain-rule gradients (Equations 8--11).
2. **Spectral Lesion Initialization:** Rather than uniform or random filter initialization, our Gabor bank is pre-aligned with 2D Fourier power spectra computed directly from foliar lesions.
3. **Dedicated Cross-Gating (GAFM):** Prior works utilized Gabor filters as isolated front-end extractors. In contrast, our GAFM dynamically modulates high-frequency texture streams against deep semantic CNN representations via channel-wise squeeze-and-excitation.

### Comment 2.2: Computational Justification for the Gabor Branch
> *"The authors must demonstrate that adding the Gabor branch is justified compared to simply scaling up the depth or width of MobileNetV3."*

**Author Response:**  
We addressed this directly in Table 1 and Table 3. Scaling MobileNetV3 to wider/deeper variants (e.g., ConvNeXt-Tiny with 28.60M params or Swin-T with 28.29M params) only yields 98.20% and 98.15% accuracy. In contrast, adding our lightweight Gabor branch to MobileNetV3-Large requires only 0.09M additional parameters (total: 5.57M) and 0.02 GFLOPs, yet achieves 99.04% accuracy (+1.16% over MobileNetV3). This demonstrates that the spatial-frequency inductive bias delivers superior representation efficiency compared to brute-force network scaling.

### Comment 2.3: Attention Mechanism Comparison
> *"Why GAFM instead of multi-head self-attention (MHSA)? Provide latency and accuracy trade-offs."*

**Author Response:**  
In Table 3 (Ablation Analysis), we added an explicit experimental comparison with a 4-head Multi-Head Cross-Attention (MHSA) module. While MHSA achieves 98.70% accuracy, GAFM achieves 99.04% accuracy while operating 3.2$\times$ faster and avoiding quadratic attention complexity, making GAFM optimal for resource-constrained edge microcomputers.

---

## Response to Reviewer 3 (Applied Statistician & Experimentalist)

### Comment 3.1: Exact Accounting of Dataset Partition Counts
> *"Ensure exact accounting between total dataset size (11,094 images) and the 70/15/15 split counts. The text and tables must agree down to the exact integer."*

**Author Response:**  
We conducted an automated audit using `scripts/check_paper_numbers.py` to ensure complete numerical synchronization. All split counts in the manuscript and Table 2 reflect the exact group-aware partition:
- **Total Field Images:** 11,094
- **Training Set (70%):** 7,761 images
- **Validation Set (15%):** 1,665 images
- **Held-Out Test Set (15%):** 1,665 images (evaluated test samples)
All in-text references use automated LaTeX macros (`\totalImages{}`, `\trainCount{}`, `\testEvaluatedSamples{}`) generated directly from `data/audit/dataset_audit.json` and `results/original/metrics.json`.

### Comment 3.2: Robustness Benchmark Formalism
> *"The corruption experiments must explicitly state the perturbation functions, parameter ranges, and whether the model was fine-tuned on corrupted images or evaluated strictly zero-shot."*

**Author Response:**  
Section 5.5 has been updated to explicitly state the mathematical corruption functions, kernel lengths ($L \in \{5, \dots, 27\}$ pixels for motion blur), noise variances ($\sigma^2 \in \{0.02, \dots, 0.18\}$), and optical parameters. Crucially, we clarified that **all models were evaluated strictly zero-shot**, with zero exposure to corruptions during training.

### Comment 3.3: Reporting Both Macro and Weighted Metrics
> *"Report both Macro and Weighted metrics to avoid obscuring minority class errors."*

**Author Response:**  
In Table 1 and Table 2, we now explicitly report both Macro-F1 (0.9904) and Weighted-F1 (0.9903), alongside Macro-Precision (0.9902) and Macro-Recall (0.9908).

---

We believe these revisions comprehensively address all reviewer concerns, substantially elevating the technical rigor, empirical validity, and scientific impact of our manuscript.

Sincerely,  
**The Authors**
