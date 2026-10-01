from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class PipelineStep(BaseModel):
    phase: int
    name: str
    status: str  # "completed", "in_progress", "todo", "failed"
    description: str
    notes: Optional[str] = None


class OverviewResponse(BaseModel):
    project_title: str
    total_images: int
    num_classes: int
    best_model_name: str
    best_accuracy: float
    best_macro_f1: float
    total_params: int
    model_size_mb: float
    cpu_latency_ms: float
    pipeline_steps: List[PipelineStep]
    dataset_summary: Dict[str, Any]
