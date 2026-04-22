@router.post("/ingest")
def ingest(file: UploadFile = File(...)):
    start = time.time()

    # validate file type
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    # save uploaded file
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

    # IMAGE CHUNKS (simulated VLM)
    image_chunks = [
        "Image: Arduino board diagram showing pin layout and microcontroller"
    ]

    # store all
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

   
      

