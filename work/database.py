import os
from logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models import Temperatures, Weather


user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB_NAME")
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
        logger.info(f"レコードを登録しました")
    except Exception as e:
        db.rollback()
        logger.info(f"レコードの登録に失敗しました: {e}")
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
        logger.info(f"レコードを登録しました")
    except Exception as e:
        db.rollback()
        logger.info(f"レコードの登録に失敗しました: {e}")
    finally:
        db.close()