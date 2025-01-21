import sys
from pathlib import Path
from fastapi import FastAPI
from datetime import datetime, date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_temperatures_by_latest, get_weather_by_date
import models
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

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
    redis = Redis(host="localhost", port=6379)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    
@app.get("/temperature")
@cache(expire=60) 
def get_temperature():
    return get_temperatures_by_latest()


@app.get("/weather")
@cache(expire=60) 
def get_weather():
    return get_weather_by_date(date.today())