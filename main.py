from fastapi import FastAPI
from src.api.routes import router   

app = FastAPI(
    title="Multimodal RAG API",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)   

