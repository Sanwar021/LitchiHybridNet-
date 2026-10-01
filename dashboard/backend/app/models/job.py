import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    job_type = Column(String, index=True)
    status = Column(String, default="queued", index=True)  # queued, running, succeeded, failed, cancelled
    command = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    exit_code = Column(Integer, nullable=True)
    log_file = Column(String, nullable=True)
    pid = Column(Integer, nullable=True)


class RunIndexModel(Base):
    __tablename__ = "runs"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    model_type = Column(String, index=True)
    seed = Column(Integer)
    status = Column(String, default="completed")
    best_epoch = Column(Integer, nullable=True)
    best_val_f1 = Column(Float, nullable=True)
    best_val_acc = Column(Float, nullable=True)
    total_params = Column(Integer, nullable=True)
    total_time_s = Column(Float, nullable=True)
    checkpoint_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
