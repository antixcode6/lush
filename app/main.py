import os
from pathlib import Path

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import setup_db 

# Get paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Data directory - use env variable if set, otherwise project root
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT))

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await setup_db() 
    yield

app = FastAPI(
    title="Lush - A minimalist blogging platform",
    description="A minimilast, self hostable, blogging platform.",
    version="0.0.1",
    lifespan=lifespan
)

