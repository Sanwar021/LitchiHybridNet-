import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import PROJECT_NAME, VERSION, API_PREFIX, PROJECT_ROOT, WORKSPACE_ROOT, DASHBOARD_DIR
from .core.database import init_db
from .routers import overview, dataset, runs, jobs, results, stats, ablations, robustness, efficiency, explain, predict, paper, system

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Also ensure DB initialized immediately
init_db()

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Research-grade REST & SSE API for LitchiHybridNet training, evaluation, explainability, and paper assets.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file mounts
fig_dir = PROJECT_ROOT / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static/figures", StaticFiles(directory=str(fig_dir)), name="figures")

tab_dir = PROJECT_ROOT / "tables"
tab_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static/tables", StaticFiles(directory=str(tab_dir)), name="tables")

# Include Routers
app.include_router(overview.router, prefix=API_PREFIX)
app.include_router(dataset.router, prefix=API_PREFIX)
app.include_router(runs.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)
app.include_router(results.router, prefix=API_PREFIX)
app.include_router(stats.router, prefix=API_PREFIX)
app.include_router(ablations.router, prefix=API_PREFIX)
app.include_router(robustness.router, prefix=API_PREFIX)
app.include_router(efficiency.router, prefix=API_PREFIX)
app.include_router(explain.router, prefix=API_PREFIX)
app.include_router(predict.router, prefix=API_PREFIX)
app.include_router(paper.router, prefix=API_PREFIX)
app.include_router(system.router, prefix=API_PREFIX)


# Mount built React frontend if it exists
frontend_dist = DASHBOARD_DIR / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="frontend-assets")
    
    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
    def serve_frontend(full_path: str):
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "project": PROJECT_NAME,
            "version": VERSION,
            "docs": "/docs",
            "health": "ok"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard.backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
