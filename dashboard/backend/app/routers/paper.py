from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..services.asset_service import AssetService
from ..core.config import PROJECT_ROOT

router = APIRouter(prefix="/paper", tags=["Paper Assets"])


@router.get("/figures")
def get_paper_figures():
    return AssetService.get_figures()


@router.get("/tables")
def get_paper_tables():
    return AssetService.get_tables()


@router.get("/checklist")
def get_paper_checklist():
    return AssetService.get_paper_checklist()


@router.get("/bib")
def get_bibtex():
    bib_file = PROJECT_ROOT / "paper" / "references.bib"
    if bib_file.exists():
        with open(bib_file, "r", encoding="utf-8") as f:
            return {"bibtex": f.read()}
    return {
        "bibtex": """@article{litchi_hybridnet_2026,
  title={LitchiHybridNet: Hybrid CNN and Learnable Gabor-Filter Texture Fusion for Field-Condition Litchi Leaf Disease Detection},
  author={Research Team},
  journal={Computers and Electronics in Agriculture},
  year={2026}
}"""
    }
