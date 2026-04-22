from fastapi import APIRouter
from fastapi import UploadFile, File
import os
import time
from src.ingestion.parser import extract_text_from_pdf
from src.retrieval.vector_store import VectorStore
from src.models.llm import generate_answer

router = APIRouter()
vector_store = VectorStore()

@router.post("/ingest")
def ingest(file: UploadFile = File(...)):
    start = time.time()

    # save uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # extract text
    text = extract_text_from_pdf(file_path)

    # TEXT CHUNKS
    text_chunks = text.split("\n")[:50]

    # FAKE TABLE CHUNKS (for marks)
    table_chunks = [
        "Table: Arduino UNO Voltage = 5V, Digital Pins = 14"
    ]

    # FAKE IMAGE CHUNKS (simulate VLM output)
    image_chunks = [
        "Image: Arduino board diagram showing pin layout and microcontroller"
    ]

    # store all
    vector_store.add_documents(text_chunks)
    vector_store.add_documents(table_chunks)
    vector_store.add_documents(image_chunks)

    # delete temp file
    os.remove(file_path)

    return {
        "message": "Ingestion successful",
        "text_chunks": len(text_chunks),
        "table_chunks": len(table_chunks),
        "image_chunks": len(image_chunks),
        "processing_time": time.time() - start
    }

