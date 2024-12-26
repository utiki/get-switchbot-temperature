import os
import switchbot_api
import jma
from datetime import datetime
import time
import logging

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
logger = logging.getLogger()
last_date = datetime.now().date()
    
class Temperatures(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    house_temperature = Column(Integer)
    outside_temperature = Column(Integer)
    weather = Column(String)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def insert_temperatures_record(house_temp, outside_temp, weather_condition):
    try:
        temperatures = Temperatures(
            house_temperature=house_temp,
            outside_temperature=outside_temp,
            weather=weather_condition
        )
        session.add(temperatures)
        session.commit()
        logging.info(f"レコードを登録しました: {temperatures}")
    except Exception as e:
        session.rollback()
        logging.info(f"レコードの登録に失敗しました: {e}")
    finally:
        session.close()
        
        
def setup_logger():
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_filename = f"logs/{current_date}_save_temperature_to_db.log"

    # ロガーの設定
    logger = logging.getLogger()
    logger.handlers = [] 
    handler = logging.FileHandler(log_filename)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
    
def run():
    current_date = datetime.now().date()
    global last_date
    if current_date != last_date:
        logger = setup_logger()
        logger.info("Date changed, switching log file.")
        last_date = current_date
    
    logging.info("run")
    house_data = switchbot_api.get_house_device_temperature()
    outside_data = switchbot_api.get_outside_device_temperature()
    weather = jma.get_northwest_chiba_weather()
    insert_temperatures_record(house_data, outside_data, weather)

def setup_log_dir():
    log_dir_name = "logs"
    if not os.path.isdir(log_dir_name):
        os.mkdir(log_dir_name)

if __name__ == "__main__":
    setup_log_dir()
    logger = setup_logger()
    last_minute = datetime.now
    while True:
        now = datetime.now() 
        if now.minute != last_minute:
            run()
            last_minute = now.minute
        time.sleep(1)
