from fastapi import FastAPI
from app.clovaOCR import router as clova_router
from app.alaram import router as alaram
app = FastAPI()
app.include_router(clova_router)
app.include_router(alaram)
