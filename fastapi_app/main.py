import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from datetime import date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_temperatures_by_latest, get_weather_by_date
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
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
def get_temperature():
    temperature = get_temperatures_by_latest()
    if temperature == 400:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    return temperature


@app.get("/weather")
def get_weather():
    weather =  get_weather_by_date(date.today())
    if weather == 400:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    return weather