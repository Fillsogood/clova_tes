from fastapi import HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from app.dtos.alaram_dto import AlarmRequestDTO, SiteAlarmDTO, AlarmScenarioDTO
from itertools import groupby
from operator import itemgetter
import hmac
import hashlib
import base64
import time
import requests
import os

load_dotenv()
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


async def service_get_alarms():
    alarm_data = []
    for i, access_key in enumerate(NCP_ACCESSKEY):
        try:
            scenarios = call_ncp_api(access_key, NCP_SECRETKEY[i], "GET", URI)
            for scenario in scenarios:
                alarm_data.append(AlarmScenarioDTO(
                    site=NCP_SITENAME[i],
                    scenario_id=str(scenario.get("scenarioId")),
                    name=scenario.get("name", "Unknown"),
                    url=scenario.get("url", "No URL"),
                    alarm_status=str(scenario.get("serviceYn", "Unknown"))
                ).dict())
        except HTTPException as e:
            alarm_data.append({
                "site": NCP_SITENAME[i],
                "error": str(e.detail)
            })
    grouped_alarms = {}
    for key, group in groupby(sorted(alarm_data, key=itemgetter("site")), key=itemgetter("site")):
        grouped_alarms[key] = list(group)
    return grouped_alarms
