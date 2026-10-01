import sys
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from ..core.database import get_db
from ..models.job import JobModel
from ..schemas.jobs import JobCreate, JobResponse
from ..services.job_manager import JobManager
from ..services.stream_service import stream_log_file

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/train", response_model=JobResponse)
def start_train_job(req: JobCreate, db: Session = Depends(get_db)):
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--model", req.model_name or "hybrid",
        "--epochs", str(req.epochs or 25),
        "--seeds", *(str(s) for s in (req.seeds or [42]))
    ]
    job = JobManager.create_and_start_job(db, job_type="train", command_args=cmd)
    return JobResponse(
        id=job.id,
        job_type=job.job_type,
        status=job.status,
        command=job.command,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        log_file=job.log_file,
        pid=job.pid
    )


@router.post("/{job_type}", response_model=JobResponse)
def start_generic_job(job_type: str, db: Session = Depends(get_db)):
    if job_type == "eval":
        cmd = [sys.executable, "scripts/run_experiment.py", "--model", "hybrid"]
    elif job_type == "paper":
        cmd = ["latexmk", "-pdf", "main.tex"]
    elif job_type == "benchmark":
        cmd = [sys.executable, "-c", "print('Running full latency benchmark...')"]
    else:
        cmd = [sys.executable, "-c", f"print('Executing pipeline phase: {job_type}')"]

    job = JobManager.create_and_start_job(db, job_type=job_type, command_args=cmd)
    return JobResponse(
        id=job.id,
        job_type=job.job_type,
        status=job.status,
        command=job.command,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        log_file=job.log_file,
        pid=job.pid
    )


@router.get("", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    JobManager.check_jobs_status(db)
    jobs = db.query(JobModel).order_by(JobModel.created_at.desc()).all()
    return [
        JobResponse(
            id=j.id,
            job_type=j.job_type,
            status=j.status,
            command=j.command,
            created_at=j.created_at.isoformat(),
            started_at=j.started_at.isoformat() if j.started_at else None,
            finished_at=j.finished_at.isoformat() if j.finished_at else None,
            exit_code=j.exit_code,
            log_file=j.log_file,
            pid=j.pid
        )
        for j in jobs
    ]


@router.get("/{job_id}/logs/stream")
def stream_job_logs(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job or not job.log_file:
        raise HTTPException(status_code=404, detail="Job or log file not found")
    return EventSourceResponse(stream_log_file(job.log_file))


@router.post("/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    success = JobManager.cancel_job(db, job_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not cancel job (may not be active)")
    return {"message": "Job cancelled successfully", "job_id": job_id}
