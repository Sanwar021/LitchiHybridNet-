import io
import base64
import numpy as np
import cv2
from PIL import Image
from typing import Tuple


class RobustnessService:
    @staticmethod
    def apply_corruption(image_bytes: bytes, corruption_type: str, severity: int) -> Tuple[bytes, str]:
        """Applies field corruption at severity 1-5."""
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        severity = max(1, min(5, severity))

        if corruption_type == "motion_blur":
            kernel_size = 3 + severity * 2
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
            kernel /= kernel_size
            corrupted = cv2.filter2D(img_np, -1, kernel)

        elif corruption_type == "gaussian_noise":
            sigma = severity * 12
            noise = np.random.normal(0, sigma, img_np.shape).astype(np.float32)
            corrupted = np.clip(img_np.astype(np.float32) + noise, 0, 255).astype(np.uint8)

        elif corruption_type in ["solar_glare", "brightness"]:
            factor = 1.0 + (severity * 0.15)
            corrupted = np.clip(img_np.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        elif corruption_type == "jpeg_compression":
            quality = max(5, 100 - severity * 18)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, enc = cv2.imencode(".jpg", cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR), encode_param)
            corrupted = cv2.cvtColor(cv2.imdecode(enc, 1), cv2.COLOR_BGR2RGB)

        else:
            corrupted = img_np

        # Output bytes and base64
        _, buffer = cv2.imencode(".png", cv2.cvtColor(corrupted, cv2.COLOR_RGB2BGR))
        out_bytes = buffer.tobytes()
        b64 = f"data:image/png;base64,{base64.b64encode(out_bytes).decode('utf-8')}"
        return out_bytes, b64
