import __main__
from datetime import datetime
import logging

logger = logging.getLogger()

def setup_logger():
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_filename = f"logs/{current_date}.log"
    
    logger = logging.getLogger()
    logger.handlers = [] 
    handler = logging.FileHandler(log_filename)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)