from fastapi import FastAPI
from api.routes import router   # ✅ NO src

app = FastAPI()

app.include_router(router)
