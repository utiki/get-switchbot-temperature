import os
import jma
import time
from datetime import datetime
from logger import setup_logger, logger
import switchbot_api
from database import insert_temperatures_record, insert_weather_record

last_date = datetime.now().date()

def on_date_change():
    current_date = datetime.now().date()
    global last_date
    if current_date != last_date:
        setup_logger()
        logger.info("Date changed, switching log file.")
        insert_weather_record(jma.get_northwest_chiba_weather())
        last_date = current_date

def run():
    on_date_change()
    logger.info("run")
    house_data = switchbot_api.get_house_device_temperature()
    outside_data = switchbot_api.get_outside_device_temperature()
    insert_temperatures_record(house_data, outside_data)

def setup_log_dir():
    log_dir_name = "logs"
    if not os.path.isdir(log_dir_name):
        os.mkdir(log_dir_name)

def init():
    setup_log_dir()
    setup_logger()
    
if __name__ == "__main__":
    init()
    last_minute = datetime.now().minute
    insert_weather_record(jma.get_northwest_chiba_weather())
    
    while True:
        now = datetime.now() 
        if now.minute != last_minute:
            run()
            last_minute = now.minute
        time.sleep(1)
