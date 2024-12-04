from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.alaram_service import service_get_alarms
from app.dtos.alaram_dto import AlarmRequestDTO, SiteAlarmDTO, AlarmScenarioDTO

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/wms")

# WMS 값 받아서 html로 보여주는 기능
@router.get("/wmsReport", response_class=JSONResponse)
async def wms_router(request: Request):
    grouped_alarms = await service_get_alarms()
    return templates.TemplateResponse("wms_report.html", {"request": request, "grouped_alarms":grouped_alarms})
