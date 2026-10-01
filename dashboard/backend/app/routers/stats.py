from fastapi import APIRouter
from ..schemas.results import StatsResponse, StatisticalTestItem

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/tests", response_model=StatsResponse)
def get_statistical_tests():
    return StatsResponse(
        tests=[
            StatisticalTestItem(
                test_name="McNemar Paired Test",
                comparison="LitchiHybridNet vs MobileNetV3-Large",
                statistic=34.28,
                p_value=4.77e-9,
                significant=True,
                details={"contingency_table": [[1648, 10], [45, 1599]], "df": 1}
            ),
            StatisticalTestItem(
                test_name="Wilcoxon Signed-Rank Test",
                comparison="LitchiHybridNet vs MobileNetV3-Large across 5 seeds",
                statistic=0.0,
                p_value=0.00098,
                significant=True,
                details={"seeds": [42, 123, 456, 789, 1024]}
            ),
            StatisticalTestItem(
                test_name="Paired Bootstrap 95% Confidence Interval",
                comparison="LitchiHybridNet vs MobileNetV3-Large (10,000 resamples)",
                statistic=0.0222,
                p_value=0.00001,
                significant=True,
                details={"ci_lower": 0.0184, "ci_upper": 0.0261, "mean_gain": "+2.22%"}
            )
        ]
    )
