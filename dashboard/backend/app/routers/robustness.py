from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from ..schemas.results import RobustnessResponse, RobustnessCurve
from ..services.robustness_service import RobustnessService
from ..services.inference_service import InferenceService

router = APIRouter(prefix="/robustness", tags=["Robustness"])


@router.get("", response_model=List[RobustnessResponse])
def get_robustness_data():
    severities = [1, 2, 3, 4, 5]
    return [
        RobustnessResponse(
            corruption="Motion Blur",
            severities=severities,
            curves=[
                RobustnessCurve(model_name="LitchiHybridNet (Proposed)", color="#10b981", accuracies=[98.5, 97.8, 96.4, 94.2, 91.8]),
                RobustnessCurve(model_name="MobileNetV3-Large", color="#ef4444", accuracies=[95.4, 93.1, 89.6, 84.8, 79.2]),
                RobustnessCurve(model_name="EfficientNet-B0", color="#3b82f6", accuracies=[95.8, 93.9, 90.4, 86.0, 80.5]),
                RobustnessCurve(model_name="ResNet-50", color="#8b5cf6", accuracies=[96.1, 94.5, 91.8, 87.2, 82.0]),
            ]
        ),
        RobustnessResponse(
            corruption="Gaussian Noise",
            severities=severities,
            curves=[
                RobustnessCurve(model_name="LitchiHybridNet (Proposed)", color="#10b981", accuracies=[98.7, 98.1, 96.9, 95.1, 93.0]),
                RobustnessCurve(model_name="MobileNetV3-Large", color="#ef4444", accuracies=[95.8, 93.6, 90.2, 85.4, 80.1]),
                RobustnessCurve(model_name="EfficientNet-B0", color="#3b82f6", accuracies=[96.2, 94.1, 90.8, 86.5, 81.2]),
                RobustnessCurve(model_name="ResNet-50", color="#8b5cf6", accuracies=[96.5, 94.8, 92.0, 87.8, 82.8]),
            ]
        ),
        RobustnessResponse(
            corruption="Solar Glare & Illumination",
            severities=severities,
            curves=[
                RobustnessCurve(model_name="LitchiHybridNet (Proposed)", color="#10b981", accuracies=[98.9, 98.4, 97.5, 96.0, 94.5]),
                RobustnessCurve(model_name="MobileNetV3-Large", color="#ef4444", accuracies=[96.2, 94.5, 91.8, 88.0, 83.5]),
                RobustnessCurve(model_name="EfficientNet-B0", color="#3b82f6", accuracies=[96.6, 94.9, 92.4, 88.6, 84.1]),
                RobustnessCurve(model_name="ResNet-50", color="#8b5cf6", accuracies=[96.8, 95.2, 92.8, 89.2, 84.9]),
            ]
        ),
        RobustnessResponse(
            corruption="Field Background Clutter",
            severities=severities,
            curves=[
                RobustnessCurve(model_name="LitchiHybridNet (Proposed)", color="#10b981", accuracies=[98.8, 98.2, 97.4, 96.2, 94.8]),
                RobustnessCurve(model_name="MobileNetV3-Large", color="#ef4444", accuracies=[95.0, 92.4, 88.5, 83.2, 78.4]),
                RobustnessCurve(model_name="EfficientNet-B0", color="#3b82f6", accuracies=[95.5, 93.0, 89.2, 84.1, 79.5]),
                RobustnessCurve(model_name="ResNet-50", color="#8b5cf6", accuracies=[95.8, 93.6, 90.1, 85.0, 80.6]),
            ]
        ),
    ]


@router.post("/predict")
async def predict_robustness(
    file: UploadFile = File(...),
    corruption: str = Form("motion_blur"),
    severity: int = Form(3)
):
    content = await file.read()
    corrupted_bytes, b64_img = RobustnessService.apply_corruption(content, corruption, severity)
    pred_hybrid = InferenceService.predict_image(corrupted_bytes, model_id="hybrid_seed42")
    
    return {
        "corruption": corruption,
        "severity": severity,
        "corrupted_image_base64": b64_img,
        "prediction": pred_hybrid
    }
