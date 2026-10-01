import os
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from ..core.database import get_db
from ..core.config import PROJECT_ROOT
from ..models.job import RunIndexModel
from ..schemas.runs import RunSummary, RunDetail, TrainingHistorySchema
from ..services.run_registry import RunRegistry
from ..services.stream_service import stream_log_file

router = APIRouter(prefix="/runs", tags=["Runs"])


@router.get("", response_model=List[RunSummary])
def get_runs(db: Session = Depends(get_db)):
    RunRegistry.sync_runs(db)
    runs = db.query(RunIndexModel).all()
    out = []
    for r in runs:
        out.append(RunSummary(
            id=r.id,
            name=r.name,
            model_type=r.model_type,
            seed=r.seed,
            status=r.status,
            best_epoch=r.best_epoch,
            best_val_f1=r.best_val_f1,
            best_val_acc=r.best_val_acc,
            total_params=r.total_params,
            total_time_s=r.total_time_s,
            created_at=r.created_at.isoformat() if r.created_at else None,
        ))
    return out


@router.get("/{run_id}", response_model=RunDetail)
def get_run_detail(run_id: str, db: Session = Depends(get_db)):
    run = db.query(RunIndexModel).filter(RunIndexModel.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    res_dir = PROJECT_ROOT / "experiments" / "results" / run_id
    history_file = res_dir / "training_history.json"
    result_file = res_dir / "experiment_result.json"

    history_data = TrainingHistorySchema()
    test_metrics = {}

    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                history_data = TrainingHistorySchema(**json.load(f))
        except Exception:
            pass

    if result_file.exists():
        try:
            with open(result_file, "r") as f:
                d = json.load(f)
                test_metrics = d.get("test_metrics", {})
        except Exception:
            pass

    chk_path = PROJECT_ROOT / "experiments" / "checkpoints" / f"{run_id}_best.pth"

    return RunDetail(
        id=run.id,
        name=run.name,
        model_type=run.model_type,
        seed=run.seed,
        status=run.status,
        config={"backbone": "mobilenetv3_large_100", "epochs": 25, "lr": 0.001, "gabor_filters": 24},
        history=history_data,
        test_metrics=test_metrics,
        checkpoint_exists=chk_path.exists(),
        checkpoint_path=str(chk_path) if chk_path.exists() else None,
    )


@router.get("/{run_id}/stream")
def stream_run_logs(run_id: str):
    # Search for matching log
    logs_dir = PROJECT_ROOT / "experiments" / "logs"
    matching = list(logs_dir.glob(f"*{run_id}*.log"))
    if not matching:
        matching = list(logs_dir.glob("*.log"))
    
    log_path = str(matching[0]) if matching else str(logs_dir / f"{run_id}.log")
    return EventSourceResponse(stream_log_file(log_path))
