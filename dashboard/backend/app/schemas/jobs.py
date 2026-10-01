from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class JobCreate(BaseModel):
    job_type: str  # "train", "eval", "robustness", "explain", "benchmark", "paper"
    model_name: Optional[str] = "hybrid"
    seeds: Optional[List[int]] = [42]
    epochs: Optional[int] = 25
    batch_size: Optional[int] = 32
    learning_rate: Optional[float] = 0.001
    fusion_type: Optional[str] = "gated"
    gabor_learnable: Optional[bool] = True
    config_overrides: Optional[Dict[str, Any]] = None


class JobResponse(BaseModel):
    id: str
    job_type: str
    status: str  # "queued", "running", "succeeded", "failed", "cancelled"
    command: str
    created_at: str
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    exit_code: Optional[int] = None
    log_file: Optional[str] = None
    pid: Optional[int] = None
