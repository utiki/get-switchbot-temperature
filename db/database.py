import os
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
Base = declarative_base()

from models import Temperatures, Weather

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    expire_on_commit=False,
    class_ = AsyncSession,
    bind = engine
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
async def insert_temperatures_record(house_temp, outside_temp):
    try:
        async with async_session() as db:
            async with db.begin():
                temperatures = Temperatures(
                    house_temperature=house_temp,
                    outside_temperature=outside_temp,
                )
                db.add(temperatures)
                await db.commit()
    except Exception as e:    
        await db.rollback(e)    
        
async def insert_weather_record(weather_report):
    try:
        async with async_session() as db:
            async with db.begin():
                weather = Weather(
                    weather=weather_report
                )
                db.add(weather)
                await db.commit()
    except Exception as e:    
        await db.rollback(e) 


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session