import os
from pathlib import Path

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS_PATH = PROJECT_ROOT / "data" / "documents"
VECTOR_STORE_PATH = PROJECT_ROOT / "data" / "chroma"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4
MAX_REWRITES = 2
