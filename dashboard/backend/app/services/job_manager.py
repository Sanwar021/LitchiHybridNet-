import os
import sys
import uuid
import datetime
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.job import JobModel
from ..core.config import PROJECT_ROOT


class JobManager:
    _active_processes: Dict[str, subprocess.Popen] = {}

    @classmethod
    def create_and_start_job(
        cls,
        db: Session,
        job_type: str,
        command_args: list,
        log_filename: Optional[str] = None
    ) -> JobModel:
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        logs_dir = PROJECT_ROOT / "experiments" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        if not log_filename:
            log_filename = f"{job_type}_{job_id}.log"
        log_path = logs_dir / log_filename
        
        cmd_str = " ".join(command_args)
        
        job = JobModel(
            id=job_id,
            job_type=job_type,
            status="running",
            command=cmd_str,
            created_at=datetime.datetime.utcnow(),
            started_at=datetime.datetime.utcnow(),
            log_file=str(log_path),
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Launch process
        log_f = open(log_path, "w", encoding="utf-8")
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"

        proc = subprocess.Popen(
            command_args,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            cwd=str(PROJECT_ROOT),
            env=env,
            text=True
        )
        
        job.pid = proc.pid
        db.add(job)
        db.commit()
        
        cls._active_processes[job_id] = proc
        return job

    @classmethod
    def check_jobs_status(cls, db: Session):
        """Update status of all active processes."""
        for job_id, proc in list(cls._active_processes.items()):
            poll = proc.poll()
            if poll is not None:
                job = db.query(JobModel).filter(JobModel.id == job_id).first()
                if job:
                    job.status = "succeeded" if poll == 0 else "failed"
                    job.exit_code = poll
                    job.finished_at = datetime.datetime.utcnow()
                    db.add(job)
                del cls._active_processes[job_id]
        db.commit()

    @classmethod
    def cancel_job(cls, db: Session, job_id: str) -> bool:
        if job_id in cls._active_processes:
            proc = cls._active_processes[job_id]
            proc.terminate()
            job = db.query(JobModel).filter(JobModel.id == job_id).first()
            if job:
                job.status = "cancelled"
                job.finished_at = datetime.datetime.utcnow()
                db.add(job)
                db.commit()
            del cls._active_processes[job_id]
            return True
        return False
