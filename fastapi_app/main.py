import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from datetime import date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_temperatures_by_latest, get_weather_by_date
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.ping()
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
async def get_temperature():
    house_temperature = await redis_client.get("house_temperature")
    outside_temperature = await redis_client.get("outside_temperature")
    if house_temperature and outside_temperature:
        print("cache hit")
        return house_temperature, outside_temperature
    
    house_temperature, outside_temperature = get_temperatures_by_latest()
    if house_temperature == 400 and outside_temperature == 400:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    await redis_client.set("house_temperature", house_temperature, ex=60)
    await redis_client.set("outside_temperature", outside_temperature, ex=60)
    return house_temperature, outside_temperature


@app.get("/weather")
async def get_weather():
    value = await redis_client.get("weather")
    if value:
        print("cache hit")
        return value
    
    weather =  get_weather_by_date(date.today())
    if weather is None:
        raise HTTPException(status_code=400, detail="Bad Request: Missing parameter")
    await redis_client.set("weather", weather, ex=60)
    return weather