# LitchiHybridNet

**Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection**

## Overview

LitchiHybridNet is a lightweight hybrid deep learning architecture that fuses CNN semantic features with learnable Gabor texture descriptors for robust litchi leaf disease classification under real field conditions (background clutter, lighting variation, blur).

**Key contributions:**
- A `LearnableGaborConv2d` layer with differentiable, constrained parameters (theta, lambda, sigma, gamma, psi) initialized from lesion frequency analysis
- SE-style cross-gating fusion that dynamically weights CNN vs. texture features per sample
- Comprehensive evaluation on BDLitchi dataset (11 disease classes, 11,094 field images)
- Designed for on-device deployment (<5 MB model size)

## Dataset

**BDLitchi: Bangladeshi Litchi Leaf Disease Dataset**  
Source: [Mendeley Data](https://data.mendeley.com/datasets/jhb24mszdk/1)

11 classes: Black Spot, Burned Leaf, Dried Leaf, Fungal Stripe Damage, Healthy Leaf, Insect Chewing Damage, Leaf Blight Disease, Pest-Affected Dry Leaf, Red Rust Disease, White Spot, Yellow Mosaic Virus

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run Phase 0: Data audit and splitting
python scripts/phase0_data_audit.py

# Train proposed model (single seed)
python scripts/run_experiment.py --model hybrid --seeds 42 --epochs 25

# Train baseline
python scripts/run_experiment.py --model cnn_only --seeds 42 --epochs 25

# Run dashboard
streamlit run dashboard/app.py
```

## Project Structure

```
litchi-hybridnet/
  configs/            # YAML experiment configs
  data/               # raw, processed, splits/
  src/
    data/             # Dataset, DataLoader, augmentation
    models/           # LitchiHybridNet, Gabor layer, baselines
    train/            # Training engine
    eval/             # Evaluation metrics
    robustness/       # Corruption robustness tests
    explain/          # Grad-CAM, feature visualization
    deploy/           # ONNX export, quantization
    utils/            # General utilities
  experiments/        # Logs, checkpoints, results
  figures/            # Generated plots (300+ dpi)
  tables/             # Generated .csv tables
  dashboard/          # Streamlit app
  paper/              # IEEE LaTeX manuscript
  scripts/            # Phase scripts, experiment runners
  PROGRESS.md         # Running progress log
  requirements.txt
```

## Architecture

```
Input (RGB 224x224)
    +-- CNN Backbone (MobileNetV3-Large, timm) --> Semantic Features
    +-- Learnable Gabor Branch (24 trainable filters) --> Texture Features
              |
              v
    Gated Fusion (SE-style cross-gating)
              |
              v
    Classifier --> 11 Disease Classes
```

## License

MIT
