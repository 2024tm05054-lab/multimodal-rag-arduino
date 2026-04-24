from fastapi import FastAPI

app = FastAPI(
    title="Multimodal RAG API",
    docs_url="/docs",        
    redoc_url="/redoc"      
)
