import os

from fastapi.responses import HTMLResponse
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def test():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello FastAPI</title>
    </head>
    <body>
        <h1>Hello, World from FastAPI!</h1>
        <p>This is a simple HTML response.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)