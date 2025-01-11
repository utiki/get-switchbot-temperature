import sys
from pathlib import Path
from fastapi import FastAPI
from datetime import datetime, date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_temperatures_by_latest, get_weather_by_date
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "chrome-extension://lieohjopnpagdoeneecbibdaooepfici",
    "http://localhost:5173",
]

# CORS の設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/temperature")
def read_root():
    return get_temperatures_by_latest()

@app.get("/weather")
def read_root():
    return get_weather_by_date()