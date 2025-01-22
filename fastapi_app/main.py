import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from datetime import datetime, date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_temperatures_by_latest, get_weather_by_date
import models
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

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

@app.on_event("startup")
async def startup():
    redis = Redis(host="radis", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    
@app.get("/temperature")
@FastAPICache.cache(expire=60)
async def get_temperature():
    temperature = get_temperatures_by_latest()
    if temperature == 400:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    return temperature


@app.get("/weather")
async def get_weather():
    weather =  get_weather_by_date(date.today())
    if weather == 400:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    return weather