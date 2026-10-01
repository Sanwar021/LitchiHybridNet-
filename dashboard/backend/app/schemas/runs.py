from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class TrainingHistorySchema(BaseModel):
    train_loss: List[float] = []
    train_acc: List[float] = []
    train_f1: List[float] = []
    val_loss: List[float] = []
    val_acc: List[float] = []
    val_macro_f1: List[float] = []
    val_macro_precision: List[float] = []
    val_macro_recall: List[float] = []
    lr: List[float] = []
    epoch_time: List[float] = []


class RunSummary(BaseModel):
    id: str
    name: str
    model_type: str
    seed: int
    status: str  # "completed", "running", "failed"
    best_epoch: Optional[int] = None
    best_val_f1: Optional[float] = None
    best_val_acc: Optional[float] = None
    total_params: Optional[int] = None
    total_time_s: Optional[float] = None
    created_at: Optional[str] = None


class RunDetail(BaseModel):
    id: str
    name: str
    model_type: str
    seed: int
    status: str
    config: Dict[str, Any] = {}
    history: TrainingHistorySchema = TrainingHistorySchema()
    test_metrics: Dict[str, Any] = {}
    checkpoint_exists: bool = False
    checkpoint_path: Optional[str] = None
    log_tail: Optional[str] = None
