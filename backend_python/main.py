import datetime
import os

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from config.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    settings.base_api_address,
    "*"
]

class ControllerData(BaseModel):
    controller_id: int
    humidity: float
    water_tank_fullness: int
    water_pump_status: str
    water_pump_working_time: int
    info: Optional[str] = None







app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_time")
async def get_current_time():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return {
        "year": now_utc.year,
        "month": now_utc.month,
        "day": now_utc.day,
        "hour": now_utc.hour,
        "minute": now_utc.minute,
        "second": now_utc.second,
        "unixtime": int(now_utc.timestamp())
    }


@app.post("/post_data")
async def post_data(data: ControllerData):
    if not data.controller_id or not data.humidity or not data.water_tank_fullness:
        return {"error": "Missing required fields in the data."}
    print(f"Received data: {data}")
    return data


@app.get("/")
async def test():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello FastAPI!!!!!!!!!!!!!!!</title>
    </head>
    <body>
        <h1>Hello, World from FastAPI!!!!!!!!!!!!!!!!!!!</h1>
        <p>This is a simple HTML response.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

