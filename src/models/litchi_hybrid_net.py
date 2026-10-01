"""
LitchiHybridNet: Hybrid CNN + Learnable Gabor-Filter Texture Fusion Network.

Architecture:
    Input (RGB Leaf Image, 224×224)
        ├── CNN Backbone (timm: MobileNetV3/EfficientNet) → Global Semantic Features
        └── Learnable Gabor Branch (24 trainable filters) → Lesion Texture Features
                │
                ▼
        Gated Fusion Module (SE-style cross-gating)
                │
                ▼
        Classification Head → 11 Disease Classes
"""

import torch
import torch.nn as nn
import timm
from typing import Dict, Any, Optional, List

from .gabor_layer import GaborTextureBranch


class GatedFusionModule(nn.Module):
    """
    Squeeze-and-Excitation style cross-gating fusion.
    
    Learns per-channel gates that modulate the fused CNN+Gabor representation,
    allowing the network to dynamically weight semantic vs. texture features
    per sample (e.g., trust texture more for spotted diseases, semantics for blight).
    """
    
    def __init__(self, cnn_dim: int, gabor_dim: int, reduction: int = 4):
        super().__init__()
        total_dim = cnn_dim + gabor_dim
        reduced = max(16, total_dim // reduction)
        
        self.gate = nn.Sequential(
            nn.Linear(total_dim, reduced),
            nn.ReLU(inplace=True),
            nn.Linear(reduced, total_dim),
            nn.Sigmoid(),
        )
        
        # Separate branch gates for analysis
        self.cnn_dim = cnn_dim
        self.gabor_dim = gabor_dim
    
    def forward(self, f_cnn: torch.Tensor, f_gabor: torch.Tensor) -> torch.Tensor:
        f_cat = torch.cat([f_cnn, f_gabor], dim=1)
        gate_values = self.gate(f_cat)
        # Residual gating
        f_fused = f_cat * (1.0 + gate_values)
        return f_fused
    
    def get_gate_values(self, f_cnn: torch.Tensor, f_gabor: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Returns gate values split into CNN and Gabor portions for analysis."""
        f_cat = torch.cat([f_cnn, f_gabor], dim=1)
        gate_values = self.gate(f_cat)
        return {
            "cnn_gate": gate_values[:, :self.cnn_dim].mean(dim=1),
            "gabor_gate": gate_values[:, self.cnn_dim:].mean(dim=1),
            "full_gate": gate_values,
        }


class ConcatFusion(nn.Module):
    """Simple concatenation fusion (ablation baseline)."""
    
    def __init__(self, cnn_dim: int, gabor_dim: int, **kwargs):
        super().__init__()
        self.cnn_dim = cnn_dim
        self.gabor_dim = gabor_dim
    
    def forward(self, f_cnn: torch.Tensor, f_gabor: torch.Tensor) -> torch.Tensor:
        return torch.cat([f_cnn, f_gabor], dim=1)


class CrossAttentionFusion(nn.Module):
    """
    Cross-attention fusion: Gabor features attend to CNN features and vice versa.
    """
    
    def __init__(self, cnn_dim: int, gabor_dim: int, reduction: int = 4, num_heads: int = 4):
        super().__init__()
        self.cnn_dim = cnn_dim
        self.gabor_dim = gabor_dim
        total_dim = cnn_dim + gabor_dim
        
        # Project both to same dimension
        proj_dim = max(64, total_dim // reduction)
        self.proj_cnn = nn.Linear(cnn_dim, proj_dim)
        self.proj_gabor = nn.Linear(gabor_dim, proj_dim)
        
        self.cross_attn = nn.MultiheadAttention(
            embed_dim=proj_dim, num_heads=num_heads, batch_first=True
        )
        self.out_proj = nn.Linear(proj_dim * 2, total_dim)
        self.norm = nn.LayerNorm(total_dim)
    
    def forward(self, f_cnn: torch.Tensor, f_gabor: torch.Tensor) -> torch.Tensor:
        # Project
        cnn_proj = self.proj_cnn(f_cnn).unsqueeze(1)    # [B, 1, D]
        gabor_proj = self.proj_gabor(f_gabor).unsqueeze(1)  # [B, 1, D]
        
        # Cross attention (Gabor queries CNN, CNN queries Gabor)
        seq = torch.cat([cnn_proj, gabor_proj], dim=1)  # [B, 2, D]
        attn_out, _ = self.cross_attn(seq, seq, seq)     # [B, 2, D]
        
        # Concatenate attended features
        fused = attn_out.reshape(attn_out.size(0), -1)   # [B, 2*D]
        out = self.out_proj(fused)                        # [B, total_dim]
        
        # Residual
        residual = torch.cat([f_cnn, f_gabor], dim=1)
        return self.norm(out + residual)


FUSION_REGISTRY = {
    "gated": GatedFusionModule,
    "concat": ConcatFusion,
    "cross_attention": CrossAttentionFusion,
}


class LitchiHybridNet(nn.Module):
    """
    LitchiHybridNet: Hybrid CNN + Learnable Gabor Texture Fusion Network.
    
    Designed for:
    - Robust field-condition disease detection under background clutter
    - Lightweight on-device deployment (mobile/edge CPU)
    - Interpretable texture-semantic feature fusion
    """
    
    def __init__(
        self,
        num_classes: int = 11,
        backbone_name: str = "mobilenetv3_large_100",
        pretrained: bool = True,
        # Gabor branch
        gabor_out_features: int = 128,
        gabor_num_scales: int = 4,
        gabor_num_orientations: int = 6,
        gabor_kernel_size: int = 11,
        gabor_learnable: bool = True,
        gabor_min_lambda: float = 3.0,
        gabor_max_lambda: float = 15.0,
        gabor_init_lambdas: Optional[List[float]] = None,
        gabor_init_thetas: Optional[List[float]] = None,
        # Fusion
        fusion_type: str = "gated",
        fusion_reduction: int = 4,
        # Classifier
        hidden_dim: int = 256,
        dropout_rate: float = 0.3,
    ):
        super().__init__()
        self.num_classes = num_classes
        self.backbone_name = backbone_name
        self.fusion_type = fusion_type
        
        # ─── Branch A: CNN Backbone (timm) ─────────────────────────────
        self.backbone = timm.create_model(
            backbone_name,
            pretrained=pretrained,
            num_classes=0,  # Remove classifier, keep feature extractor
            global_pool="avg",
        )
        # Get CNN feature dimension
        with torch.no_grad():
            dummy = torch.randn(1, 3, 224, 224)
            cnn_dim = self.backbone(dummy).shape[1]
        self.cnn_dim = cnn_dim
        
        # ─── Branch B: Learnable Gabor Texture ─────────────────────────
        self.gabor_branch = GaborTextureBranch(
            out_features=gabor_out_features,
            num_scales=gabor_num_scales,
            num_orientations=gabor_num_orientations,
            kernel_size=gabor_kernel_size,
            learnable=gabor_learnable,
            min_lambda=gabor_min_lambda,
            max_lambda=gabor_max_lambda,
            init_lambdas=gabor_init_lambdas,
            init_thetas=gabor_init_thetas,
        )
        self.gabor_dim = gabor_out_features
        
        # ─── Fusion Module ─────────────────────────────────────────────
        fusion_cls = FUSION_REGISTRY.get(fusion_type, GatedFusionModule)
        self.fusion = fusion_cls(
            cnn_dim=cnn_dim,
            gabor_dim=gabor_out_features,
            reduction=fusion_reduction,
        )
        total_fused_dim = cnn_dim + gabor_out_features
        
        # ─── Classification Head ───────────────────────────────────────
        self.classifier = nn.Sequential(
            nn.Linear(total_fused_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, num_classes),
        )
        
        # Store features for analysis
        self._last_cnn_features = None
        self._last_gabor_features = None
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Branch A: CNN
        f_cnn = self.backbone(x)          # [B, cnn_dim]
        
        # Branch B: Gabor texture
        f_gabor = self.gabor_branch(x)    # [B, gabor_dim]
        
        # Store for analysis
        self._last_cnn_features = f_cnn.detach()
        self._last_gabor_features = f_gabor.detach()
        
        # Fusion
        f_fused = self.fusion(f_cnn, f_gabor)  # [B, cnn_dim + gabor_dim]
        
        # Classification
        logits = self.classifier(f_fused)      # [B, num_classes]
        return logits
    
    def get_embeddings(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Returns intermediate embeddings for t-SNE/UMAP visualization."""
        with torch.no_grad():
            f_cnn = self.backbone(x)
            f_gabor = self.gabor_branch(x)
            f_fused = self.fusion(f_cnn, f_gabor)
        return {
            "cnn": f_cnn,
            "gabor": f_gabor,
            "fused": f_fused,
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Returns architecture parameters and model footprint."""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        frozen_params = total_params - trainable_params
        
        # Gabor-specific params
        gabor_params = sum(p.numel() for p in self.gabor_branch.parameters() if p.requires_grad)
        gabor_learnable_filter_params = sum(
            p.numel() for name, p in self.gabor_branch.gabor.named_parameters() if p.requires_grad
        )
        
        return {
            "model_name": "LitchiHybridNet",
            "backbone": self.backbone_name,
            "gabor_branch": f"{self.gabor_branch.gabor.num_filters} Learnable Gabor Filters",
            "fusion_type": self.fusion_type,
            "cnn_dim": self.cnn_dim,
            "gabor_dim": self.gabor_dim,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "frozen_parameters": frozen_params,
            "gabor_trainable_params": gabor_params,
            "gabor_filter_params": gabor_learnable_filter_params,
            "model_size_mb": round(total_params * 4 / (1024 * 1024), 2),
            "num_classes": self.num_classes,
        }


class CNNOnlyModel(nn.Module):
    """CNN-only baseline (ablation: no Gabor branch)."""
    
    def __init__(
        self,
        num_classes: int = 11,
        backbone_name: str = "mobilenetv3_large_100",
        pretrained: bool = True,
        hidden_dim: int = 256,
        dropout_rate: float = 0.3,
    ):
        super().__init__()
        self.backbone = timm.create_model(
            backbone_name, pretrained=pretrained, num_classes=0, global_pool="avg"
        )
        with torch.no_grad():
            cnn_dim = self.backbone(torch.randn(1, 3, 224, 224)).shape[1]
        
        self.classifier = nn.Sequential(
            nn.Linear(cnn_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, num_classes),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.backbone(x))


class GaborOnlyModel(nn.Module):
    """Gabor-only baseline (ablation: no CNN branch)."""
    
    def __init__(
        self,
        num_classes: int = 11,
        gabor_out_features: int = 256,
        gabor_num_scales: int = 4,
        gabor_num_orientations: int = 6,
        gabor_kernel_size: int = 11,
        gabor_learnable: bool = True,
        hidden_dim: int = 256,
        dropout_rate: float = 0.3,
    ):
        super().__init__()
        self.gabor_branch = GaborTextureBranch(
            out_features=gabor_out_features,
            num_scales=gabor_num_scales,
            num_orientations=gabor_num_orientations,
            kernel_size=gabor_kernel_size,
            learnable=gabor_learnable,
        )
        self.classifier = nn.Sequential(
            nn.Linear(gabor_out_features, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, num_classes),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.gabor_branch(x))
