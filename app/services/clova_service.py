from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.dtos.clova_dto import OCRRequestDTO, OCRResponseDTO, ImageDataDTO
import requests
import uuid
import time
import json
from dotenv import load_dotenv
import os
# 환경 변수 로드
load_dotenv()
async def service_ocr_upload_image(image: UploadFile = File(...)):
    """
    업로드된 이미지를 CLova OCR API로 보내고 inferText 값을 반환합니다.
    """
    try:
        # 업로드된 이미지 읽기
        image_data = await image.read()
        image_name = image.filename

         # 이미지 데이터 DTO 생성
        image_dto = ImageDataDTO(
            format=image_name.split('.')[-1].lower(),
            name=image_name.split('.')[0]
        )

        # OCR 요청 DTO 생성
        request_data = OCRRequestDTO(
            images=[image_dto],
            requestId=str(uuid.uuid4()),
            version="V2",
            timestamp=int(round(time.time() * 1000))
        )

        # 요청 데이터
        payload = {
            "message": request_data.json()  # DTO를 JSON으로 직렬화
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
                # Pydantic 모델로 응답 데이터 검증 및 매핑
                ocr_response = OCRResponseDTO(**res)
                
                # inferText 값 추출
                texts = [
                    field.inferText
                    for image in ocr_response.images
                    for field in image.fields
                    if field.inferText
                ]
                return {"texts": texts, "success": True}
            except json.JSONDecodeError:
                return {"error": "Failed to parse response", "success": False}
        else:
            return {
                    "error": f"Request failed with status code: {response.status_code}",
                    "success": False
                }
    except Exception as e:
        return {"error": str(e), "success": False}
