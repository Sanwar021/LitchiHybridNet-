from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class SystemStatusResponse(BaseModel):
    cpu_percent: float
    cpu_count: int
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    gpu_available: bool
    gpu_name: Optional[str] = None
    disk_percent: float
    python_version: str
    torch_version: str
    git_commit: Optional[str] = None
    active_jobs: int
