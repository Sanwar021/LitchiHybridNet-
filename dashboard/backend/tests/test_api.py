import pytest
from fastapi.testclient import TestClient
from dashboard.backend.app.core.database import init_db
from dashboard.backend.app.main import app

init_db()
client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["health"] == "ok"


def test_overview_endpoint():
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["best_accuracy"] > 90
    assert len(data["pipeline_steps"]) == 11


def test_dataset_audit():
    response = client.get("/api/dataset/audit")
    assert response.status_code == 200
    data = response.json()
    assert data["total_images"] == 11094
    assert data["num_classes"] == 11


def test_runs_endpoint():
    response = client.get("/api/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_results_comparison():
    response = client.get("/api/results/comparison")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 7
    assert data[0]["model"].startswith("LitchiHybridNet")


def test_ablations():
    response = client.get("/api/ablations")
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_robustness():
    response = client.get("/api/robustness")
    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_efficiency():
    response = client.get("/api/efficiency")
    assert response.status_code == 200
    assert len(response.json()["rows"]) >= 6


def test_system():
    response = client.get("/api/system")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data
    assert "ram_percent" in data
