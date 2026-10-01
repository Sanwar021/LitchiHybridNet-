from fastapi import APIRouter, UploadFile, File, Form
from ..schemas.predict import PredictResponse
from ..services.inference_service import InferenceService

router = APIRouter(prefix="/predict", tags=["Inference"])


@router.post("", response_model=PredictResponse)
async def predict_image(
    file: UploadFile = File(...),
    model_id: str = Form("hybrid_seed42"),
    include_cam: bool = Form(True),
    include_gabor: bool = Form(True)
):
    content = await file.read()
    result = InferenceService.predict_image(
        image_bytes=content,
        model_id=model_id,
        include_cam=include_cam,
        include_gabor=include_gabor
    )
    return PredictResponse(**result)
