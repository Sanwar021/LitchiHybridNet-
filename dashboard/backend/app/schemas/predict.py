from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class PredictRequest(BaseModel):
    model_id: Optional[str] = "hybrid_seed42"
    backend: Optional[str] = "pytorch"  # "pytorch", "onnx", "int8"
    include_cam: Optional[bool] = True
    include_gabor: Optional[bool] = True
    cam_method: Optional[str] = "gradcam"  # "gradcam", "gradcam++", "eigencam"


class PredictResponse(BaseModel):
    model_id: str
    backend: str
    predicted_class: str
    predicted_index: int
    confidence: float
    probabilities: Dict[str, float]
    inference_time_ms: float
    gradcam_base64: Optional[str] = None
    gabor_response_base64: Optional[str] = None
    gate_values: Optional[Dict[str, float]] = None
