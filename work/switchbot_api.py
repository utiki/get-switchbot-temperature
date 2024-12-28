import time
import uuid
import hmac
import hashlib
import base64

from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import requests

def request(url):
    api_token = os.getenv('TOKEN')
    secret_token = os.getenv('CLIENT_SECRET')
    
    t = int(time.time() * 1000)
    nonce = str(uuid.uuid4())
    string_to_sign = f"{api_token}{t}{nonce}".encode('utf-8')
    secret_key = secret_token.encode('utf-8')
    signature = hmac.new(secret_key, string_to_sign, hashlib.sha256).digest()
    sign = base64.b64encode(signature).decode('utf-8').upper()

    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json",
        "t": str(t),
        "nonce": nonce,
        "sign": sign
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.status_code, response.json()
    else:
        return response.status_code, response.text
    
def request_loop(url):
    status_code, json = request(url)
    while status_code != 200:
        time.sleep(5)
        status_code, json = request(url)
    return json

def get_all_device_id():
    url = "https://api.switch-bot.com/v1.1/devices"
    return request_loop(url)
    
def get_device_status(device_id):
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    return request_loop(url)
    
def get_house_device_temperature():
    house_thermometer_id = os.getenv('HOUSE_THERMOMETER_ID')
    temperature: float  = get_device_status(house_thermometer_id)["body"]["temperature"]
    return temperature

def get_outside_device_temperature():
    outside_thermometer_id = os.getenv('OUTSIDE_THERMOMETER_ID')
    temperature: float = get_device_status(outside_thermometer_id)["body"]["temperature"]
    return temperature