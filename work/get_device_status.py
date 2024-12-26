import os
import sys
import switchbot_api
import pandas as pd

if __name__ == "__main__":
    args = sys.argv
    if (len(args) != 2):
        print("Usage: python get_switchbot_temperature.py <device_id>")
        sys.exit(1)
    device_id = args[1]
    data = switchbot_api.get_device_status(device_id)['body']
    df = pd.DataFrame([data], columns=['version','temperature', 'battery', 'humidity', 'deviceId', 'deviceType','hubDeviceId'])
    print(df.to_string(index=False))
