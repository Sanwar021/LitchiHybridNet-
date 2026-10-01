"""Quick test: verify all model architectures build and run correctly."""
import sys
sys.path.insert(0, ".")

import torch
from src.models import LitchiHybridNet, CNNOnlyModel, GaborOnlyModel

x = torch.randn(2, 3, 224, 224)

# Test Hybrid
m = LitchiHybridNet()
y = m(x)
s = m.get_summary()
print(f"LitchiHybridNet output: {y.shape}")
print(f"  Total params: {s['total_parameters']:,}")
print(f"  Trainable:    {s['trainable_parameters']:,}")
print(f"  Size:         {s['model_size_mb']} MB")
print(f"  Gabor filter params: {s['gabor_filter_params']}")

# Test CNN-only
m2 = CNNOnlyModel()
y2 = m2(x)
print(f"CNNOnlyModel output: {y2.shape}")

# Test Gabor-only
m3 = GaborOnlyModel()
y3 = m3(x)
print(f"GaborOnlyModel output: {y3.shape}")

# Test embeddings
emb = m.get_embeddings(x)
print(f"Embeddings - CNN: {emb['cnn'].shape}, Gabor: {emb['gabor'].shape}, Fused: {emb['fused'].shape}")

# Test Gabor params
params = m.gabor_branch.gabor.get_params_dict()
print(f"Gabor theta (degrees): {[f'{t:.1f}' for t in params['theta_deg']]}")
print(f"Gabor wavelengths: {[f'{w:.2f}' for w in params['wavelength']]}")

print("\nAll models OK!")
