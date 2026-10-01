from fastapi import APIRouter
from ..schemas.system import SystemStatusResponse
from ..services.system_service import SystemService
from ..core.config import PROJECT_ROOT

router = APIRouter(tags=["System"])


@router.get("/system", response_model=SystemStatusResponse)
def get_system():
    stats = SystemService.get_system_stats()
    return SystemStatusResponse(**stats)


@router.get("/progress")
def get_progress_markdown():
    prog_file = PROJECT_ROOT / "PROGRESS.md"
    content = ""
    if prog_file.exists():
        with open(prog_file, "r", encoding="utf-8") as f:
            content = f.read()
    return {"progress_markdown": content}
