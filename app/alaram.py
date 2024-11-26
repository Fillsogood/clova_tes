from fastapi import FastAPI, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from itertools import groupby
from operator import itemgetter
import hmac
import hashlib
import base64
import time
import requests
import json
import os

load_dotenv()
router = APIRouter()
templates = Jinja2Templates(directory="templates")
# test 관리에서 KPFIS부분은 root계정 api accesskey 및 secretkey 발급했으니 추후에 WMS(web service Monitoring System)만 api key 만들어서 넣기
# NCP API 인증 정보


# 환경 변수 가져오기
NCP_ACCESSKEY = os.getenv("NCP_ACCESSKEY").split(",")
NCP_SECRETKEY = os.getenv("NCP_SECRETKEY").split(",")
NCP_SITENAME = os.getenv("NCP_SITENAME").split(",")
URI = os.getenv("URI")
BASE_URL = os.getenv("BASE_URL")

# signature 변환
def generate_signature(access_key, secret_key, method, uri):
    
    timestamp = str(int(time.time() * 1000))
    message = f"{method} {uri}\n{timestamp}\n{access_key}"
    signature = base64.b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    return timestamp, signature

# api 불러오기
def call_ncp_api(access_key, secret_key, method, uri):
    
    timestamp, signature = generate_signature(access_key, secret_key, method, uri)
    headers = {
        "Content-Type": "application/json",
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-apigw-signature-v2": signature,
    }
    response = requests.request(method, f"{BASE_URL}{uri}", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# WMS 값 받아서 html로 보여주는 기능
@router.get("/wmsReport", response_class=JSONResponse)
async def root(request: Request):
    alarm_data = []
    for i, access_key in enumerate(NCP_ACCESSKEY):
        try:
            scenarios = call_ncp_api(access_key, NCP_SECRETKEY[i], "GET", URI)
            for scenario in scenarios:
                alarm_data.append({
                    "site": NCP_SITENAME[i],
                    "scenario_id": scenario.get("scenarioId"),
                    "name": scenario.get("name", "Unknown"),
                    "url": scenario.get("url", "No URL"),
                    "alarm_status": scenario.get("serviceYn", "Unknown")
                })
        except Exception as e:
            alarm_data.append({
                "site": NCP_SITENAME[i],
                "error": str(e.detail)
            })
    # 데이터 그룹화
    grouped_alarms = {}
    for key, group in groupby(sorted(alarm_data, key=itemgetter("site")), key=itemgetter("site")):
        grouped_alarms[key] = list(group)
    return templates.TemplateResponse(
        "wms_report.html",
        {
            "request": request,
            "grouped_alarms": grouped_alarms
        }
    )
            


# api 받은거 json으로 결과값 보는 용도
@router.get("/api/alarms", response_class=JSONResponse)
async def api():
    results = {}
    for i, access_key in enumerate(NCP_ACCESSKEY):
        try:
            scenarios = call_ncp_api(access_key, NCP_SECRETKEY[i], "GET", URI)
            results[NCP_SITENAME[i]] = scenarios
        except HTTPException as e:
            results[NCP_SITENAME[i]] = {"error": e.detail}
    return JSONResponse(content=results)
