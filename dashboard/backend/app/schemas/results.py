from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class BenchmarkRow(BaseModel):
    model: str
    backbone: str
    params_m: float
    flops_m: float
    accuracy_mean: float
    accuracy_std: float
    macro_f1_mean: float
    macro_f1_std: float
    mcc_mean: float
    latency_cpu_ms: float
    size_mb: float


class ConfusionMatrixResponse(BaseModel):
    classes: List[str]
    matrix: List[List[int]]
    normalized_matrix: List[List[float]]


class PerClassMetric(BaseModel):
    class_name: str
    precision: float
    recall: float
    f1_score: float
    support: int


class PerClassMetricsResponse(BaseModel):
    classes: List[str]
    metrics: List[PerClassMetric]


class AblationItem(BaseModel):
    variant: str
    params_m: float
    accuracy_mean: float
    accuracy_std: float
    macro_f1_mean: float
    macro_f1_std: float


class AblationResponse(BaseModel):
    group: str
    items: List[AblationItem]


class RobustnessCurve(BaseModel):
    model_name: str
    color: str
    accuracies: List[float]


class RobustnessResponse(BaseModel):
    corruption: str
    severities: List[int]
    curves: List[RobustnessCurve]


class EfficiencyRow(BaseModel):
    model_variant: str
    format: str
    device: str
    batch_size: int
    params_m: float
    flops_m: float
    size_mb: float
    latency_mean_ms: float
    latency_p95_ms: float
    accuracy: float


class EfficiencyResponse(BaseModel):
    rows: List[EfficiencyRow]


class StatisticalTestItem(BaseModel):
    test_name: str
    comparison: str
    statistic: float
    p_value: float
    significant: bool
    details: Optional[Dict[str, Any]] = None


class StatsResponse(BaseModel):
    tests: List[StatisticalTestItem]
