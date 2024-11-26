import requests
import uuid
import time
import json
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Templates 설정
templates = Jinja2Templates(directory="templates")

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def ocr_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/clova-ocr", response_class=HTMLResponse)
async def ocr_form(request: Request):
    return templates.TemplateResponse("ocr_form.html", {"request": request})

@router.post("/ocr")
async def upload_image(request: Request, image: UploadFile = File(...)):
    """
    업로드된 이미지를 CLova OCR API로 보내고 inferText 값을 반환합니다.
    """
    try:
        # 업로드된 이미지 읽기
        image_data = await image.read()
        image_name = image.filename

        # CLova OCR API 요청 JSON 구성
        request_json = {
            "images": [
                {
                    "format": image_name.split('.')[-1].lower(),  # 이미지 포맷 (예: jpg, png)
                    "name": image_name.split('.')[0]  # 이미지 이름
                }
            ],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(round(time.time() * 1000))
        }

        # 요청 데이터
        payload = {
            "message": json.dumps(request_json)  # JSON 메시지
        }

        # 업로드 파일 구성
        files = {
            "file": (image_name, image_data, image.content_type)
        }

        # 요청 헤더 구성
        headers = {
            "X-OCR-SECRET": os.getenv("CLOVA_SECRET_API_KEY")
        }

        # CLova OCR API 요청 보내기
        response = requests.post(
            os.getenv("CLOVA_API_URL"),
            headers=headers,
            data=payload,
            files=files
        )

        # 응답 처리
        if response.status_code == 200:
            try:
                res = response.json()
                # Extract all `inferText` values from `fields`
                texts = [
                    field.get("inferText")
                    for image in res.get("images", [])
                    for field in image.get("fields", [])
                    if field.get("inferText")
                ]
                return templates.TemplateResponse(
                    "ocr_form.html",
                    {"request": request, "texts": texts, "success": True}
                )
            except json.JSONDecodeError:
                return templates.TemplateResponse(
                    "ocr_form.html",
                    {
                        "request": request,
                        "error": "Failed to parse response",
                        "success": False
                    }
                )
        else:
            return templates.TemplateResponse(
                "ocr_form.html",
                {
                    "request": request,
                    "error": f"Request failed with status code: {response.status_code}",
                    "success": False
                }
            )
    except Exception as e:
        return templates.TemplateResponse(
            "ocr_form.html",
            {"request": request, "error": str(e), "success": False}
        )