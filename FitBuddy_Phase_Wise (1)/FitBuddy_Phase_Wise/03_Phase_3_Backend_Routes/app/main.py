from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="FitBuddy – AI Fitness Plan Generator", version="1.0.0", description="AI-assisted fitness planning demo built with FastAPI, Jinja2, SQLite and Gemini.")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api")
def api_root():
    settings = get_settings()
    return {"name": settings.app_name, "docs": "/docs", "health": "/api/health"}
