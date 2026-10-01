import os
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = APP_DIR.parent
DASHBOARD_DIR = BACKEND_DIR.parent
PROJECT_ROOT = DASHBOARD_DIR.parent  # c:/Users/Fame IT/Videos/rwn/438/litchi-hybridnet
WORKSPACE_ROOT = PROJECT_ROOT.parent

DB_PATH = BACKEND_DIR / "dashboard.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

API_PREFIX = "/api"
PROJECT_NAME = "LitchiHybridNet Control Center"
VERSION = "1.0.0"
