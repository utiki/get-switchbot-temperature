import os
from fastapi import HTTPException
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models import Temperatures, Weather

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def insert_temperatures_record(house_temp, outside_temp):
    try:
        db = SessionLocal()
        temperatures = Temperatures(
            house_temperature=house_temp,
            outside_temperature=outside_temp,
        )
        db.add(temperatures)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
        
        
def insert_weather_record(weather_report):
    try:
        db = SessionLocal()
        weather = Weather(
            weather=weather_report
        )
        db.add(weather)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()


def get_temperatures_by_latest():
    try:
        db = SessionLocal()
        record = db.query(Temperatures).order_by(desc(Temperatures.id)).first()
        return record.house_temperature, record.outside_temperature
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


def get_weather_by_date(date):
    try:
        db = SessionLocal()
        record = db.query(Weather).filter(
            func.date(Weather.created_at)  == date
        ).first()
        return record.weather
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
