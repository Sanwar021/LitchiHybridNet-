from fastapi import APIRouter
from ..schemas.results import EfficiencyResponse, EfficiencyRow

router = APIRouter(prefix="/efficiency", tags=["Efficiency"])


@router.get("", response_model=EfficiencyResponse)
def get_efficiency():
    return EfficiencyResponse(
        rows=[
            EfficiencyRow(model_variant="LitchiHybridNet (PyTorch FP32)", format="PyTorch", device="CPU", batch_size=1, params_m=5.57, flops_m=235.0, size_mb=21.25, latency_mean_ms=38.4, latency_p95_ms=42.1, accuracy=99.04),
            EfficiencyRow(model_variant="LitchiHybridNet (ONNX FP32)", format="ONNX", device="CPU", batch_size=1, params_m=5.57, flops_m=235.0, size_mb=21.18, latency_mean_ms=26.2, latency_p95_ms=29.5, accuracy=99.04),
            EfficiencyRow(model_variant="LitchiHybridNet (ONNX INT8 Quantized)", format="ONNX INT8", device="CPU", batch_size=1, params_m=5.57, flops_m=235.0, size_mb=5.40, latency_mean_ms=14.8, latency_p95_ms=17.2, accuracy=98.72),
            EfficiencyRow(model_variant="MobileNetV3-Large", format="PyTorch", device="CPU", batch_size=1, params_m=5.40, flops_m=219.0, size_mb=20.60, latency_mean_ms=32.1, latency_p95_ms=35.4, accuracy=96.82),
            EfficiencyRow(model_variant="EfficientNet-B0", format="PyTorch", device="CPU", batch_size=1, params_m=5.30, flops_m=390.0, size_mb=20.20, latency_mean_ms=52.0, latency_p95_ms=57.8, accuracy=97.15),
            EfficiencyRow(model_variant="ShuffleNetV2 1.0x", format="PyTorch", device="CPU", batch_size=1, params_m=2.28, flops_m=146.0, size_mb=8.70, latency_mean_ms=24.8, latency_p95_ms=28.1, accuracy=95.12),
            EfficiencyRow(model_variant="ResNet-50", format="PyTorch", device="CPU", batch_size=1, params_m=25.56, flops_m=4120.0, size_mb=97.50, latency_mean_ms=142.6, latency_p95_ms=158.0, accuracy=97.40),
            EfficiencyRow(model_variant="ConvNeXt-Tiny", format="PyTorch", device="CPU", batch_size=1, params_m=28.60, flops_m=4500.0, size_mb=109.20, latency_mean_ms=168.0, latency_p95_ms=185.0, accuracy=97.80),
        ]
    )
