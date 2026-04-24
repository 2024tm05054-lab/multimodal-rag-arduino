from fastapi import APIRouter, UploadFile, File
from src.ingestion.parser import extract_text_from_pdf
from src.retrieval.vector_store import VectorStore
from src.models.llm import generate_answer

router = APIRouter()

vector_store = None   # placeholder
