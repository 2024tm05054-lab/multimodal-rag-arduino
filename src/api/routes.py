from fastapi import APIRouter
from src.ingestion.parser import extract_text_from_pdf
from src.retrieval.vector_store import VectorStore
from src.models.llm import generate_answer

router = APIRouter()

vector_store = VectorStore()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ingest")
def ingest():
    text = extract_text_from_pdf("sample_documents/arduino_manual.pdf")

    # split text into chunks
    chunks = text.split("\n")[:50]

    vector_store.add_documents(chunks)

    return {"message": "Document ingested"}

@router.post("/query")
def query(q: str):
    results = vector_store.search(q)
    answer = generate_answer(q, results)

    return {
        "query": q,
        "answer": answer,
        "sources": results
    }
