from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class DuplicateStats(BaseModel):
    exact_hash_duplicates: int
    near_duplicate_groups: int
    cross_class_duplicates: int


class SplitStats(BaseModel):
    train: int
    val: int
    test: int
    total: int
    group_aware: bool
    leakage_count: int


class DatasetAuditResponse(BaseModel):
    total_images: int
    num_classes: int
    classes: List[str]
    class_distribution: Dict[str, int]
    resolution_stats: Dict[str, float]
    duplicates: DuplicateStats
    splits: SplitStats


class SplitStatsResponse(BaseModel):
    splits: SplitStats
    classes: List[str]
    per_class_split: Dict[str, Dict[str, int]]
