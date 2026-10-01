# LitchiHybridNet: Experimental Evaluation & Comparative Study

### Model: Hybrid CNN and Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection

#### 1. Executive Summary
This study presents **LitchiHybridNet**, an on-device hybrid deep learning architecture designed for robust classification of field-condition litchi leaf diseases under severe background clutter (soil, ambient foliage, varying sun angles). By coupling a lightweight CNN backbone (MobileNetV3) with a 24-channel lesion-tuned Gabor spatial-frequency filter bank and cross-gating channel attention, the network effectively suppresses environmental clutter while capturing high-frequency lesion edge signatures.

Two independent experiments were conducted on the **BDLitchi: Bangladeshi Litchi Leaf Disease Dataset**:
1. **Original Dataset**: 11,094 natural field images across 11 classes.
2. **Augmented Dataset**: 16,500 balanced images across 11 classes.

#### 2. Overall Performance Comparison

| Metric            | Original Dataset             | Augmented Dataset                  | Delta (Aug - Orig)   |
|:------------------|:-----------------------------|:-----------------------------------|:---------------------|
| Dataset           | BDLitchi Raw (11,094 images) | BDLitchi Augmented (16,500 images) | -                    |
| Test Accuracy     | 99.04%                       | 97.94%                             | -1.10%               |
| Macro F1-Score    | 0.9904                       | 0.9794                             | -0.0110              |
| Weighted F1-Score | 0.9903                       | 0.9794                             | -0.0109              |
| Macro Precision   | 0.9902                       | 0.9800                             | -0.0102              |
| Macro Recall      | 0.9908                       | 0.9794                             | -0.0114              |
| Test Samples      | 1665                         | 2475                               | +810                 |

#### 3. Per-Class F1-Score Breakdown

| Class Name             |   Orig F1 |   Aug F1 |   F1 Gain |   Orig Recall |   Aug Recall |
|:-----------------------|----------:|---------:|----------:|--------------:|-------------:|
| Black Spot             |    0.9639 |   0.96   |   -0.0039 |        0.9363 |       0.96   |
| Burned Leaf            |    0.9887 |   0.9934 |    0.0047 |        0.9943 |       1      |
| Dried Leaf             |    1      |   0.9956 |   -0.0044 |        1      |       1      |
| Fungal Stripe Damage   |    0.9964 |   0.9774 |   -0.019  |        1      |       0.96   |
| Healthy Leaf           |    0.9966 |   0.9773 |   -0.0194 |        1      |       0.9556 |
| Insect Chewing Damage  |    0.9971 |   0.9698 |   -0.0273 |        0.9943 |       1      |
| Leaf Blight Disease    |    0.9966 |   0.9802 |   -0.0163 |        1      |       0.9911 |
| Pest-Affected Dry Leaf |    0.9887 |   0.9773 |   -0.0114 |        0.9924 |       0.9556 |
| Red Rust Disease       |    0.9845 |   0.9823 |   -0.0022 |        0.9815 |       0.9867 |
| White Spot             |    0.9814 |   0.976  |   -0.0054 |        1      |       0.9956 |
| Yellow Mosaic Virus    |    1      |   0.9842 |   -0.0158 |        1      |       0.9689 |

#### 4. Key Architectural Insights
- **Traditional CV Gabor Filters**: Act as deterministic spatial-frequency bandpass filters that isolate characteristic lesion frequencies (punctate spots, fungal stripes, necrosis edges) without requiring millions of trainable parameters.
- **Cross-Gating Fusion**: The Squeeze-and-Excitation gating enables Gabor texture energies to modulate CNN semantic features, dynamically suppressing non-lesion background noise (soil, shadows, unrelated foliage).
- **Edge / On-Device Deployment**: With only ~1.37M total parameters and ~5 MB memory footprint, LitchiHybridNet is fully optimized for real-time edge CPU deployment on handheld agricultural scanners or mobile phones.
