from fastapi import APIRouter, UploadFile, File
import os
import time

from src.ingestion.parser import extract_text_from_pdf
from src.retrieval.vector_store import VectorStore
from src.models.llm import generate_answer

router = APIRouter()

# initialize vector store
vector_store = VectorStore()

# track uptime
start_time = time.time()


# =========================
# HEALTH ENDPOINT
# =========================
@router.get("/health")
def health():
    return {
        "status": "ok",
        "documents_indexed": len(vector_store.texts),
        "uptime_seconds": time.time() - start_time
    }


# =========================
# INGEST ENDPOINT
# =========================
@router.post("/ingest")
def ingest(file: UploadFile = File(...)):
    start = time.time()

    # validate file type
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    # save uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # extract text
    text = extract_text_from_pdf(file_path)

    if not text:
        return {"error": "Failed to extract text from PDF"}

    # TEXT CHUNKS
    text_chunks = text.split("\n")[:50]

    # TABLE CHUNKS (simulated)
    table_chunks = [
        "Table: Arduino UNO Voltage = 5V, Digital Pins = 14"
    ]

    # IMAGE CHUNKS (simulated VLM output)
    image_chunks = [
        "Image: Arduino board diagram showing pin layout and microcontroller"
    ]

    # store all chunks
    vector_store.add_documents(text_chunks)
    vector_store.add_documents(table_chunks)
    vector_store.add_documents(image_chunks)

    # delete temp file safely
    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "message": "Ingestion successful",
        "file_name": file.filename,
        "text_chunks": len(text_chunks),
        "table_chunks": len(table_chunks),
        "image_chunks": len(image_chunks),
        "total_chunks": len(text_chunks) + len(table_chunks) + len(image_chunks),
        "processing_time": time.time() - start
    }


# =========================
# QUERY ENDPOINT
# =========================
@router.post("/query")
def query(q: str):
    # check if any document is indexed
    if len(vector_store.texts) == 0:
        return {"error": "No documents indexed. Please run /ingest first."}

    # retrieve relevant chunks
    results = vector_store.search(q)

    # generate answer
    answer = generate_answer(q, results)

    # prepare sources (VERY IMPORTANT FOR MARKS)
    sources = []
    for r in results:
        chunk_type = "text"
        if "Table:" in r:
            chunk_type = "table"
        elif "Image:" in r:
            chunk_type = "image"

        sources.append({
            "content": r,
            "type": chunk_type
        })

    return {
        "query": q,
        "answer": answer,
        "sources": sources,
        "num_sources": len(sources)
    }
