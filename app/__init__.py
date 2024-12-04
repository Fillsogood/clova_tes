from fastapi import FastAPI
from app.routers.alaram_router import router as alaram_router
from app.routers.view_router import router as view_router
from app.routers.clova_router import router as clova_router
app = FastAPI()
app.include_router(clova_router)
app.include_router(view_router)
app.include_router(alaram_router)
