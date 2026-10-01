# LitchiHybridNet Makefile

.PHONY: help install dashboard dashboard-dev dashboard-test dashboard-build reproduce test paper

help:
	@echo "Available commands:"
	@echo "  make dashboard       - Starts unified FastAPI + React Dashboard on port 8000"
	@echo "  make dashboard-dev   - Starts Vite React dev server on port 5173"
	@echo "  make dashboard-test  - Runs pytest test suite for dashboard API backend"
	@echo "  make dashboard-build - Builds production React bundle"
	@echo "  make reproduce       - Runs multi-seed training & evaluation pipeline"
	@echo "  make test            - Runs all project unit and regression tests"

install:
	pip install -r requirements.txt
	cd dashboard/frontend && npm install

dashboard-build:
	cd dashboard/frontend && npm run build

dashboard: dashboard-build
	python -m uvicorn dashboard.backend.app.main:app --host 0.0.0.0 --port 8000

dashboard-dev:
	cd dashboard/frontend && npm run dev

dashboard-test:
	python -m pytest dashboard/backend/tests/test_api.py -v

test:
	python -m pytest tests/ -v

reproduce:
	python scripts/run_experiment.py --model hybrid --seeds 42 123 456

paper:
	python scripts/make_auto_numbers.py
	python scripts/make_paper_tables.py
	python scripts/make_paper_figures.py
	python scripts/verify_references.py
	python scripts/check_paper_numbers.py
	@echo "All paper assets, tables, figures, numbers, and references verified."
