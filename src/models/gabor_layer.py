"""
Learnable Gabor Filter Layer for LitchiHybridNet.

Unlike fixed Gabor banks, this module makes theta, lambda, sigma, gamma, psi
trainable parameters (constrained to valid ranges via sigmoid/softplus).
Initialized from lesion frequency analysis (Phase 1) or default values.

Mathematical formulation:
    g(x, y) = exp(-(x'^2 + γ²·y'^2) / (2σ²)) · cos(2π·x'/λ + ψ)
    where:
        x' =  x·cos(θ) + y·sin(θ)
        y' = -x·sin(θ) + y·cos(θ)

All parameters are differentiable — gradients flow through the Gabor construction.
"""

import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List


class LearnableGaborConv2d(nn.Module):
    """
    Learnable 2D Gabor filter bank as a differentiable convolution layer.
    
    Parameters are constrained to physically meaningful ranges:
        θ (theta): [0, π) — orientation
        λ (lambda): [λ_min, λ_max] — wavelength (spatial frequency)
        σ (sigma): [σ_min, σ_max] — Gaussian envelope width
        γ (gamma): [0.1, 1.0] — spatial aspect ratio
        ψ (psi): [0, 2π) — phase offset
    """
    
    def __init__(
        self,
        in_channels: int = 1,
        num_scales: int = 4,
        num_orientations: int = 6,
        kernel_size: int = 11,
        stride: int = 1,
        padding: Optional[int] = None,
        learnable: bool = True,
        # Initialization ranges
        min_lambda: float = 3.0,
        max_lambda: float = 15.0,
        sigma_ratio: float = 0.56,
        gamma_init: float = 0.5,
        # Parameter value initializations (from Phase 1, if available)
        init_lambdas: Optional[List[float]] = None,
        init_thetas: Optional[List[float]] = None,
    ):
        super().__init__()
        
        self.in_channels = in_channels
        self.num_scales = num_scales
        self.num_orientations = num_orientations
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding if padding is not None else kernel_size // 2
        self.num_filters = num_scales * num_orientations
        self.learnable = learnable
        
        # Parameter ranges for constraining via sigmoid
        self.lambda_min = min_lambda
        self.lambda_max = max_lambda
        self.sigma_min = 1.0
        self.sigma_max = max_lambda * 1.2
        self.gamma_min = 0.1
        self.gamma_max = 1.0
        
        # ─── Initialize parameters ────────────────────────────────────
        # θ: orientations (logit space, mapped to [0, π) via sigmoid * π)
        if init_thetas is not None:
            theta_init = torch.tensor(init_thetas, dtype=torch.float32)
        else:
            theta_init = torch.linspace(0, math.pi * (1 - 1/num_orientations), num_orientations)
            theta_init = theta_init.repeat(num_scales)
        # Convert to logit space: theta = sigmoid(raw) * π → raw = logit(theta/π)
        theta_logits = torch.log(theta_init / math.pi / (1 - theta_init / math.pi + 1e-8) + 1e-8)
        
        # λ: wavelengths 
        if init_lambdas is not None:
            lambda_init = torch.tensor(init_lambdas, dtype=torch.float32)
        else:
            lambda_init = torch.linspace(min_lambda, max_lambda, num_scales)
            lambda_init = lambda_init.repeat_interleave(num_orientations)
        # Map to logit space for [lambda_min, lambda_max]
        lambda_norm = (lambda_init - min_lambda) / (max_lambda - min_lambda + 1e-8)
        lambda_logits = torch.log(lambda_norm / (1 - lambda_norm + 1e-8) + 1e-8)
        
        # σ: derived from λ initially (σ = sigma_ratio * λ)
        sigma_init = sigma_ratio * lambda_init
        sigma_norm = (sigma_init - self.sigma_min) / (self.sigma_max - self.sigma_min + 1e-8)
        sigma_logits = torch.log(sigma_norm / (1 - sigma_norm + 1e-8) + 1e-8)
        
        # γ: aspect ratio
        gamma_init_t = torch.full((self.num_filters,), gamma_init)
        gamma_norm = (gamma_init_t - self.gamma_min) / (self.gamma_max - self.gamma_min + 1e-8)
        gamma_logits = torch.log(gamma_norm / (1 - gamma_norm + 1e-8) + 1e-8)
        
        # ψ: phase offset (0 for even-symmetric)
        psi_init = torch.zeros(self.num_filters)
        
        if learnable:
            self.theta_raw = nn.Parameter(theta_logits)
            self.lambda_raw = nn.Parameter(lambda_logits)
            self.sigma_raw = nn.Parameter(sigma_logits)
            self.gamma_raw = nn.Parameter(gamma_logits)
            self.psi = nn.Parameter(psi_init)
        else:
            self.register_buffer("theta_raw", theta_logits)
            self.register_buffer("lambda_raw", lambda_logits)
            self.register_buffer("sigma_raw", sigma_logits)
            self.register_buffer("gamma_raw", gamma_logits)
            self.register_buffer("psi", psi_init)
        
        # Fixed spatial grid
        half = kernel_size // 2
        y, x = torch.meshgrid(
            torch.arange(-half, half + 1, dtype=torch.float32),
            torch.arange(-half, half + 1, dtype=torch.float32),
            indexing="ij"
        )
        self.register_buffer("grid_x", x)  # [K, K]
        self.register_buffer("grid_y", y)  # [K, K]
    
    @property
    def theta(self) -> torch.Tensor:
        """Constrained orientation: [0, π)"""
        return torch.sigmoid(self.theta_raw) * math.pi
    
    @property
    def wavelength(self) -> torch.Tensor:
        """Constrained wavelength: [λ_min, λ_max]"""
        return self.lambda_min + torch.sigmoid(self.lambda_raw) * (self.lambda_max - self.lambda_min)
    
    @property
    def sigma(self) -> torch.Tensor:
        """Constrained sigma: [σ_min, σ_max]"""
        return self.sigma_min + torch.sigmoid(self.sigma_raw) * (self.sigma_max - self.sigma_min)
    
    @property
    def gamma(self) -> torch.Tensor:
        """Constrained aspect ratio: [γ_min, γ_max]"""
        return self.gamma_min + torch.sigmoid(self.gamma_raw) * (self.gamma_max - self.gamma_min)
    
    def _build_kernels(self) -> torch.Tensor:
        """
        Construct Gabor filter kernels from current parameters.
        Returns: [num_filters, 1, K, K]
        """
        theta = self.theta       # [N]
        lam = self.wavelength    # [N]
        sig = self.sigma         # [N]
        gam = self.gamma         # [N]
        psi = self.psi           # [N]
        
        # Expand grids: [N, K, K]
        x = self.grid_x.unsqueeze(0)  # [1, K, K]
        y = self.grid_y.unsqueeze(0)  # [1, K, K]
        
        cos_t = torch.cos(theta).view(-1, 1, 1)
        sin_t = torch.sin(theta).view(-1, 1, 1)
        
        x_theta = x * cos_t + y * sin_t
        y_theta = -x * sin_t + y * cos_t
        
        sig = sig.view(-1, 1, 1)
        gam = gam.view(-1, 1, 1)
        lam = lam.view(-1, 1, 1)
        psi = psi.view(-1, 1, 1)
        
        # Gabor formula
        gaussian = torch.exp(-0.5 * (x_theta**2 + (gam * y_theta)**2) / (sig**2))
        sinusoidal = torch.cos(2 * math.pi * x_theta / lam + psi)
        
        kernels = gaussian * sinusoidal  # [N, K, K]
        
        # Zero-DC (remove mean to ensure lighting invariance)
        kernels = kernels - kernels.mean(dim=(-2, -1), keepdim=True)
        
        # L2 normalize
        norm = kernels.norm(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        kernels = kernels / norm
        
        # Shape for conv: [N, 1, K, K] → repeat for in_channels
        kernels = kernels.unsqueeze(1)  # [N, 1, K, K]
        if self.in_channels > 1:
            kernels = kernels.repeat(1, self.in_channels, 1, 1)
        
        return kernels
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [B, C, H, W] input tensor
        Returns:
            [B, num_filters, H', W'] Gabor response maps
        """
        kernels = self._build_kernels()  # [N, C, K, K]
        return F.conv2d(x, kernels, stride=self.stride, padding=self.padding)
    
    def get_params_dict(self) -> dict:
        """Return current parameter values (detached) for logging."""
        return {
            "theta_deg": (self.theta * 180 / math.pi).detach().cpu().numpy().tolist(),
            "wavelength": self.wavelength.detach().cpu().numpy().tolist(),
            "sigma": self.sigma.detach().cpu().numpy().tolist(),
            "gamma": self.gamma.detach().cpu().numpy().tolist(),
            "psi": self.psi.detach().cpu().numpy().tolist(),
        }


class GaborTextureBranch(nn.Module):
    """
    Full Gabor texture processing branch:
    RGB → Grayscale → LearnableGaborConv2d → BN → ReLU → Pool → DW-PW Conv → GlobalPool → FC
    
    Produces a compact texture descriptor vector.
    """
    
    def __init__(
        self,
        out_features: int = 128,
        num_scales: int = 4,
        num_orientations: int = 6,
        kernel_size: int = 11,
        learnable: bool = True,
        min_lambda: float = 3.0,
        max_lambda: float = 15.0,
        init_lambdas: Optional[List[float]] = None,
        init_thetas: Optional[List[float]] = None,
    ):
        super().__init__()
        
        # Fixed luminance projection (ITU-R BT.601)
        self.rgb_to_gray = nn.Conv2d(3, 1, kernel_size=1, bias=False)
        with torch.no_grad():
            self.rgb_to_gray.weight.data = torch.tensor(
                [[[[0.2989]], [[0.5870]], [[0.1140]]]]
            ).float()
        self.rgb_to_gray.weight.requires_grad = False
        
        # Learnable Gabor filter bank
        self.gabor = LearnableGaborConv2d(
            in_channels=1,
            num_scales=num_scales,
            num_orientations=num_orientations,
            kernel_size=kernel_size,
            stride=2,
            learnable=learnable,
            min_lambda=min_lambda,
            max_lambda=max_lambda,
            init_lambdas=init_lambdas,
            init_thetas=init_thetas,
        )
        num_gabor = self.gabor.num_filters
        
        # Feature processing
        self.bn_gabor = nn.BatchNorm2d(num_gabor)
        self.act = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Depthwise-separable conv
        self.conv_dw = nn.Conv2d(num_gabor, num_gabor, kernel_size=3, padding=1,
                                  groups=num_gabor, bias=False)
        self.conv_pw = nn.Conv2d(num_gabor, 64, kernel_size=1, bias=False)
        self.bn2 = nn.BatchNorm2d(64)
        
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Sequential(
            nn.Linear(64, out_features),
            nn.BatchNorm1d(out_features),
            nn.ReLU(inplace=True),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gray = self.rgb_to_gray(x)           # [B, 1, H, W]
        g = self.gabor(gray)                  # [B, N, H/2, W/2]
        g = self.act(self.bn_gabor(g))
        g = self.pool1(g)                     # [B, N, H/4, W/4]
        g = self.conv_dw(g)
        g = self.act(self.bn2(self.conv_pw(g)))  # [B, 64, H/4, W/4]
        feat = self.global_pool(g).flatten(1)    # [B, 64]
        return self.fc(feat)                     # [B, out_features]
    
    def get_gabor_responses(self, x: torch.Tensor) -> torch.Tensor:
        """Returns raw Gabor responses for visualization."""
        with torch.no_grad():
            gray = self.rgb_to_gray(x)
            return self.gabor(gray)
