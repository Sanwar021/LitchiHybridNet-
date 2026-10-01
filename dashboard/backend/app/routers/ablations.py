from typing import List
from fastapi import APIRouter
from ..schemas.results import AblationResponse, AblationItem

router = APIRouter(prefix="/ablations", tags=["Ablations"])


@router.get("", response_model=List[AblationResponse])
def get_ablations():
    return [
        AblationResponse(
            group="Branch Contribution",
            items=[
                AblationItem(variant="Gabor Texture Only", params_m=0.26, accuracy_mean=86.80, accuracy_std=0.45, macro_f1_mean=0.8640, macro_f1_std=0.0050),
                AblationItem(variant="CNN Backbone Only (MobileNetV3)", params_m=5.40, accuracy_mean=96.82, accuracy_std=0.35, macro_f1_mean=0.9675, macro_f1_std=0.0030),
                AblationItem(variant="Fixed Gabor + CNN (Concat)", params_m=5.57, accuracy_mean=97.52, accuracy_std=0.28, macro_f1_mean=0.9745, macro_f1_std=0.0025),
                AblationItem(variant="Learnable Gabor + CNN (Concat)", params_m=5.57, accuracy_mean=98.22, accuracy_std=0.22, macro_f1_mean=0.9815, macro_f1_std=0.0020),
                AblationItem(variant="LitchiHybridNet (Learnable + Gated)", params_m=5.57, accuracy_mean=99.04, accuracy_std=0.12, macro_f1_mean=0.9904, macro_f1_std=0.0010),
            ]
        ),
        AblationResponse(
            group="Fusion Mechanism",
            items=[
                AblationItem(variant="Simple Addition", params_m=5.55, accuracy_mean=97.10, accuracy_std=0.30, macro_f1_mean=0.9710, macro_f1_std=0.0028),
                AblationItem(variant="Channel Concatenation", params_m=5.57, accuracy_mean=98.22, accuracy_std=0.22, macro_f1_mean=0.9815, macro_f1_std=0.0020),
                AblationItem(variant="Multi-Head Cross-Attention", params_m=5.75, accuracy_mean=98.70, accuracy_std=0.18, macro_f1_mean=0.9870, macro_f1_std=0.0016),
                AblationItem(variant="SE-Gated Cross-Fusion (Proposed)", params_m=5.57, accuracy_mean=99.04, accuracy_std=0.12, macro_f1_mean=0.9904, macro_f1_std=0.0010),
            ]
        ),
        AblationResponse(
            group="Gabor Filter Scales & Orientations",
            items=[
                AblationItem(variant="2 Scales × 4 Orientations (8 filters)", params_m=5.56, accuracy_mean=97.60, accuracy_std=0.30, macro_f1_mean=0.9750, macro_f1_std=0.0028),
                AblationItem(variant="3 Scales × 6 Orientations (18 filters)", params_m=5.56, accuracy_mean=98.45, accuracy_std=0.20, macro_f1_mean=0.9840, macro_f1_std=0.0018),
                AblationItem(variant="4 Scales × 6 Orientations (24 filters - Default)", params_m=5.57, accuracy_mean=99.04, accuracy_std=0.12, macro_f1_mean=0.9904, macro_f1_std=0.0010),
                AblationItem(variant="5 Scales × 8 Orientations (40 filters)", params_m=5.59, accuracy_mean=99.08, accuracy_std=0.14, macro_f1_mean=0.9907, macro_f1_std=0.0012),
            ]
        )
    ]
