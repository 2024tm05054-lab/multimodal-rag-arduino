from fastapi import FastAPI
from src.api.routes import router   # ✅ USE src

app = FastAPI()
app.include_router(router)
