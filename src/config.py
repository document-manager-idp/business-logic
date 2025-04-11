import os
from pathlib import Path

class Config:
    SRC_DIR = Path(__file__).resolve().parent
    UPLOAD_DIR = SRC_DIR.parent / "uploads"
    LOGS_DIR = SRC_DIR.parent / "logs"
    DEBUG = True
    CORS_HEADERS = 'Content-Type'

    SPACY_MODEL = "ro_core_news_lg"
    MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

Config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
