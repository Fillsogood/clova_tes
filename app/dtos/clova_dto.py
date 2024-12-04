from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
import uuid
import time

class ImageDataDTO(BaseModel):
    format: str  # 이미지 파일 형식 (예: jpg, png)
    name: str    # 이미지 이름
# 요청 DTO
class OCRRequestDTO(BaseModel):
    images: List[ImageDataDTO]  # 이미지 데이터 리스트
    requestId: str = str(uuid.uuid4())  # 고유 요청 ID
    version: str = "V2"
    timestamp: int = int(round(time.time() * 1000))

# 응답 데이터 내부 구조 DTO
class OCRFieldDTO(BaseModel):
    inferText: Optional[str]  # 추출된 텍스트 값
    boundingPoly: Union[List[dict], dict]  # 텍스트 위치 정보 (Optional)

# 이미지 응답 DTO
class OCRImageDTO(BaseModel):
    fields: List[OCRFieldDTO]  # OCR로 분석된 필드 목록

# 최종 응답 DTO
class OCRResponseDTO(BaseModel):
    images: List[OCRImageDTO]  # 이미지 응답 데이터
