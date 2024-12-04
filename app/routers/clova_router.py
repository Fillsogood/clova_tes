from fastapi import APIRouter, Request,UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import List

from fastapi import UploadFile

import json
from app.dtos.clova_dto import OCRRequestDTO, OCRResponseDTO
from app.services.clova_service import service_ocr_upload_image
router = APIRouter()
templates = Jinja2Templates(directory="app/templates/clova")


@router.get("/clova", response_class=HTMLResponse)
async def clova_form_router(request: Request):
    return templates.TemplateResponse("clova.html", {"request": request})
# 
@router.get("/clova-ocr-from", response_class=HTMLResponse)
async def clova_ocr_router(request: Request):
    return templates.TemplateResponse("ocr_form.html", {"request": request})

@router.post("/ocr-upload")
async def upload_image(request: Request,image: UploadFile = File(...)):

    data = await service_ocr_upload_image(image)
    return templates.TemplateResponse(
                    "ocr_form.html",
                    {"request": request, "texts": data["texts"], "success": data["success"]}
                )
