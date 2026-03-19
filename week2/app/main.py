from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes
from . import db

init_db()

app = FastAPI(title="Action Item Extractor")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# --- Refactored backend main API for clarity and robustness ---

from fastapi import Body
from pydantic import BaseModel

# Define Pydantic schemas for clarity and type safety
class ExtractRequest(BaseModel):
    text: str

class ActionItemsResponse(BaseModel):
    action_items: list[str]

# Example improved extraction endpoint using schemas and robust error handling
@app.post("/extract_action_items", response_model=ActionItemsResponse)
def extract_action_items_api(request: ExtractRequest):
    """
    Extract action items from the given text using classic heuristics.
    """
    try:
        from .services.extract import extract_action_items
        items = extract_action_items(request.text)
        return ActionItemsResponse(action_items=items)
    except Exception as e:
        # Log the error for debugging in real code
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")


@app.post("/extract_action_items_llm", response_model=ActionItemsResponse)
def extract_action_items_llm_api(request: ExtractRequest):
    """
    Extract action items using LLM-powered extraction.
    """
    try:
        from .services.extract import extract_action_items_llm
        items = extract_action_items_llm(request.text)
        return ActionItemsResponse(action_items=items)
    except ImportError:
        # ollama may not be installed on all environments
        raise HTTPException(status_code=503, detail="LLM extraction is unavailable - ensure Ollama is running and installed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {e}")

# Additional app configuration cleanup (optional, for real-life projects)
# You can register exception handlers, middlewares or CORS settings here
# For simplicity, left out unless explicitly needed by the assignment
