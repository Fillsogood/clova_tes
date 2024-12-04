from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union

# 요청 DTO
class AlarmRequestDTO(BaseModel):
    access_key: str
    secret_key: str
    uri: str

# 응답 DTO
class AlarmScenarioDTO(BaseModel):
    site: str
    scenario_id: int
    name: Optional[str] = "Unknown"
    url: Optional[HttpUrl] = None
    alarm_status: Optional[bool] = "Unknown"

class SiteAlarmDTO(BaseModel):
    site: str
    alarms: List[Union[AlarmScenarioDTO, dict]]  # dict를 포함시켜 오류 데이터를 허용
