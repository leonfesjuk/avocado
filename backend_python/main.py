import datetime
import os

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from resources.conections import add_humidity_data, create_db_engine
from sqlalchemy.orm import Session
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


engine = create_db_engine(settings.database_url)



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
    print(f"Received data: {data}")
    try:
        with Session(engine) as session:
            success = add_humidity_data(
                session=session,
                controller_id=data.controller_id,
                humidity_value=int(data.humidity)
            )
            if success:
                session.commit()
                print("Data successfully committed to the database.")
                return {"message": "Data saved successfully"}
            else:
                session.rollback()
                print("Failed to add data, transaction rolled back.")
                return {"message": "Failed to save data"}
    except Exception as e:
        print(f"An error occurred during database operation: {e}")
        return {"message": "An error occurred", "error": str(e)}


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

