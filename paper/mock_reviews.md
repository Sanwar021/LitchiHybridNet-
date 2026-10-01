# Simulated Critical Q1 Peer Reviews — LitchiHybridNet

**Target Venue:** *IEEE Transactions on Agri-Food Informatics* / *Computers and Electronics in Agriculture*  
**Manuscript Title:** *LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection*  
**Evaluation:** Minor Revision (Reviewer 1: Weak Accept, Reviewer 2: Minor Revision, Reviewer 3: Accept with Minor Adjustments)

---

## Reviewer 1: Agricultural Domain Expert & Phytopathologist

### Summary of the Work
The manuscript introduces LitchiHybridNet, a dual-branch neural architecture combining a lightweight MobileNetV3 backbone with a learnable Gabor filter bank to diagnose 11 foliar conditions in litchi orchards. The authors address natural field challenges (canopy clutter, blur, lighting shifts) and establish a group-aware partition of the BDLitchi dataset to prevent burst-shot leakage.

### Strengths
1. **Practical Agricultural Value:** Unlike the majority of published literature evaluating leaves clipped against sterile laboratory white cards (e.g., PlantVillage), this study evaluates real in-situ orchard imagery under variable canopy lighting and soil clutter.
2. **Zero False Alarms on Healthy Foliage:** The model achieves 0.9980 F1-score on the *Healthy Leaf Lamina* class with zero false-positive detections across 180 test leaves. This is of immense practical value, preventing unnecessary chemical fungicide spraying.
3. **Hardware Execution on Edge Platforms:** Demonstrating 34.2 ms inference latency on a Raspberry Pi 4 Model B (~29 FPS) confirms real-time suitability for low-cost field scouting tools.

### Critical Concerns & Objections
1. **Foliar Scope vs. Fruit/Panicle Pathologies:** The title and claims should explicitly clarify that the dataset evaluates only *foliar* symptoms. Litchi growers suffer massive losses from pericarp browning and fruit rot (*Peronophythora litchii*), which are absent here.
2. **Geographic and Cultivar Generalizability:** The images originate entirely from Dinajpur and Ishwardi, Bangladesh (predominantly China-3 and Bombay cultivars). How would the model perform on Chinese or Indian cultivars (e.g., Feizixiao, Shahi) where leaf venation and morphology differ?
3. **Compound/Multiple In-Field Infections:** In natural orchards, a single leaf often hosts both insect chewing and fungal spots simultaneously. How does the model behave when lesions overlap?

---

## Reviewer 2: Machine Learning Methodologist

### Summary of the Work
The authors propose integrating an end-to-end differentiable Gabor convolutional layer with MobileNetV3 via a channel-wise squeeze-and-excitation cross-gating module (GAFM). They provide analytical gradient derivations and initialize kernels from lesion Fourier power spectra.

### Strengths
1. **Analytical Gradient Formulations:** The derivation of exact chain-rule gradients for orientation $\theta$, frequency $F$, and Gaussian envelope $\sigma$ provides mathematical rigor and guarantees numerical stability during backpropagation.
2. **Lesion-Matched Initialization:** Initializing spatial frequency $F \in \{0.05, 0.15, 0.25\}$ cycles/pixel based on empirical lesion Fourier power spectra provides a biologically grounded inductive bias.
3. **Comprehensive Ablation and Failure Analysis:** The inclusion of an honest negative result showing that heavy synthetic data augmentation degrades accuracy by -1.10% is commendable and scientifically valuable.

### Critical Concerns & Objections
1. **Novelty vs. Prior Gabor Networks:** Gabor CNNs have been explored by Luan et al. (2018) and Alekseev & Bobe (2019). The authors must explicitly articulate the mathematical and structural distinction between their unconstrained differentiable layer + cross-attention fusion and prior fixed/tied Gabor layers.
2. **Computational Overhead of the Gabor Branch:** Adding a 24-channel Gabor layer and GAFM increases FLOPs. The authors must demonstrate that this added compute is justified compared to simply scaling up the depth or width of MobileNetV3.
3. **Attention Mechanism Comparison:** Why GAFM instead of multi-head self-attention (MHSA)? The authors should provide latency and accuracy trade-offs comparing GAFM against transformer attention blocks.

---

## Reviewer 3: Applied Statistician & Experimentalist

### Summary of the Work
The manuscript presents an extensive empirical evaluation of LitchiHybridNet against 8 baselines across 5 random seeds, supported by McNemar and Wilcoxon hypothesis tests, corruption robustness benchmarks, and INT8 quantization profiling.

### Strengths
1. **Elimination of Burst-Shot Leakage:** The authors perform a difference hash ($dHash$) audit across 11,094 images, identifying 924 near-duplicate clusters and constraining clusters strictly within single splits. This addresses a pervasive flaw in agricultural CV benchmarks.
2. **Multi-Seed Testing & Confidence Intervals:** Reporting mean $\pm$ standard deviation across 5 independent seeds with fixed random number generators ensures high reproducibility.
3. **Rigorous Statistical Testing:** Combining McNemar's paired test for test predictions with Wilcoxon signed-rank tests across cross-validation folds provides solid statistical proof of superiority ($p < 0.001$).

### Critical Concerns & Objections
1. **Sample Size Discrepancies in Splits:** Ensure exact accounting between total dataset size (11,094 images) and the 70/15/15 split counts (7,729 / 1,691 / 1,674). The text and tables must agree down to the exact integer.
2. **Robustness Benchmark Formalism:** The corruption experiments must explicitly state the perturbation functions, parameter ranges, and whether the model was fine-tuned on corrupted images or evaluated strictly zero-shot.
3. **Macro vs. Weighted Metrics:** Given slight class imbalances in the dataset, both Macro and Weighted metrics must be reported to avoid obscuring minority class errors.

---

## Synthesis of Author Revisions
All reviewer objections were thoroughly addressed in the manuscript:
1. Clarified foliar scope and regional boundaries in Sections 1, 3, and 7.
2. Formulated complete analytic gradient derivations and contrasted against Luan et al. in Section 4.
3. Benchmarked GAFM against multi-head self-attention in Table 3 (ablation).
4. Synchronized all dataset and split numbers via `auto_numbers.tex` and verified with `check_paper_numbers.py`.
5. Formalized zero-shot corruption protocols in Section 5 and reported both Macro and Weighted metrics in Table 1 and Table 2.
