from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Mock variables (replace these with actual values)
NCP_ACCESSKEY = ["key1", "key2"]  # List of access keys
NCP_SECRETKEY = ["secret1", "secret2"]  # List of secret keys
NCP_SITENAME = ["Site 1", "Site 2"]  # List of site names
URI = "your_api_endpoint_here"  # Replace with your API URI

# Mock function for API call (replace with actual API logic)
def call_ncp_api(access_key, secret_key, method, uri):
    return [
        {"scenarioId": "1", "name": "Scenario 1", "url": "http://example.com", "serviceYn": "Active"},
        {"scenarioId": "2", "name": "Scenario 2", "url": "http://example2.com", "serviceYn": "Inactive"}
    ]

@app.get("/alarms2", response_class=HTMLResponse)
async def root(request: Request):
    res: List[dict] = []
    for i, access_key in enumerate(NCP_ACCESSKEY):

        try:
            scenarios = call_ncp_api(access_key, NCP_SECRETKEY[i], "GET", URI)
            for scenario in scenarios:
                response = {
                    "scenario_id": scenario.get("scenarioId"),
                    "scenario_name": scenario.get("name", "Unknown"),
                    "scenario_url": scenario.get("url", "No URL"),
                    "alarm_status": scenario.get("serviceYn", "Unknown"),
                }
                res.append(response)
        except Exception as e:
            return templates.TemplateResponse(
                "alaram.html",
                {
                    "request": request,
                    "error": f"Request failed with status code: {e}",
                    "success": False
                },
            )

    return templates.TemplateResponse(
        "alaram.html",{
            "request": request,
            "alarms": res,
            "success": True
        }
    )
