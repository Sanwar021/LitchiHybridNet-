# Formal Submission Cover Letter

**Date:** October 1, 2026  

**To:**  
The Editor-in-Chief  
*IEEE Transactions on Agri-Food Informatics* (or *Computers and Electronics in Agriculture*, Elsevier)  

**Subject:** Submission of Original Research Manuscript:  
*"LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection"*  

Dear Editor-in-Chief,

We are pleased to submit our original research manuscript titled **"LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection"** for consideration for publication as a regular research article in *IEEE Transactions on Agri-Food Informatics*.

### Context and Significance of the Work
Automating foliar disease diagnosis in litchi (*Litchi chinensis* Sonn.) orchards is vital for safeguarding crop yields and food security across South and Southeast Asia. However, operational field imagery introduces complex background canopy clutter, solar illumination shifts, and optical motion blur that cause standard deep convolutional networks and vision transformers to suffer severe performance degradation.

In this manuscript, we present **LitchiHybridNet**, a lightweight, dual-branch deep learning framework that couples high-frequency spatial-frequency representations from an end-to-end differentiable **Learnable Gabor Convolutional Bank** with deep semantic abstractions from a lightweight MobileNetV3 backbone. Features are dynamically recalibrated via the **Gabor Attention Fusion Module (GAFM)**, which suppresses background foliage clutter and accentuates lesion boundaries.

### Key Technical Contributions and Empirical Findings
1. **Biological Frequency Inductive Bias:** We formulate a 24-channel learnable Gabor filter bank with exact analytic chain-rule gradients for backpropagation, initialized from 2D Fourier power spectra of natural litchi lesions.
2. **Leakage-Free Benchmark Audit:** We conduct a perceptual difference hash ($dHash$) audit across the 11,094-image BDLitchi dataset, resolving 924 burst-shot near-duplicate clusters to establish a verified, group-aware 70/15/15 stratified partition.
3. **State-of-the-Art Accuracy:** Across 5 random seeds, LitchiHybridNet attains **99.04% Top-1 accuracy** and **0.9904 Macro-F1**, statistically outperforming ResNet-50, EfficientNet-B0, MobileNetV3, Swin-Transformer, and ConvNeXt-Tiny ($p < 0.001$).
4. **Adverse Field Robustness:** Under severity-5 optical motion blur, LitchiHybridNet retains 85.4% accuracy, maintaining a **+12.6% advantage** over standard CNNs.
5. **Real-Time Agricultural Edge Deployment:** Post-training INT8 quantization yields an ultra-compact **5.40 MB** model executing in **14.8 ms** on commodity x86 CPUs and **34.2 ms (~29 FPS)** on a low-cost Raspberry Pi 4 Model B, confirming direct feasibility for handheld field scouting and autonomous robotic spraying.

### Declarations
- This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere.
- All authors have reviewed and approved the submitted version of the manuscript and agree with its submission.
- The authors declare no competing financial or non-financial conflicts of interest.
- All experimental source code, pre-trained models, and dataset audit manifests are made publicly available under the MIT License at https://github.com/Sanwar021/LitchiHybridNet-.git.

### Suggested Reviewers
We propose the following independent domain experts who possess appropriate technical expertise in agricultural computer vision, Gabor filtering, and edge deep learning:

1. **Prof. Dr. [NAME 1]**  
   *Affiliation:* Department of Agricultural Engineering / Computer Vision Lab, [UNIVERSITY 1]  
   *Expertise:* Deep learning for crop phenotyping, field-condition plant pathology, lightweight CNNs.  
   *Email:* [EMAIL 1]  

2. **Dr. [NAME 2]**  
   *Affiliation:* Institute of Smart Agriculture, [INSTITUTE 2]  
   *Expertise:* Spatial-frequency image processing, Gabor wavelets, explainable AI in agriculture.  
   *Email:* [EMAIL 2]  

3. **Prof. [NAME 3]**  
   *Affiliation:* Department of Computer Science & Engineering, [UNIVERSITY 3]  
   *Expertise:* Embedded edge computing, model quantization, ONNX Runtime optimization for robotics.  
   *Email:* [EMAIL 3]  

Thank you very much for your time, consideration, and coordination of the peer-review process.

Sincerely,

**Rawan Hasan** (Author & Principal Investigator)  
Email: `rawan.hasan@example.com`
  
