import sys
from pathlib import Path
from fastapi import FastAPI, Depends
from datetime import date

sys.path.append(str(Path(__file__).parent.parent / "db"))
from database import get_session
from models import Temperatures, Weather
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

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
async def read_temperature(session: AsyncSession = Depends(get_session)):
    record = await session.execute(
        select(Temperatures).order_by(
            desc(Temperatures.id)
        )    
    )
    temperatures = record.scalars().first()
    return temperatures.house_temperature, temperatures.outside_temperature

@app.get("/weather")
async def read_weather(session: AsyncSession = Depends(get_session)):
    record = await session.execute(select(Weather).where(
        func.date(Weather.created_at) == date.today()
    ))
    weather = record.scalars().first()
    return weather.weather