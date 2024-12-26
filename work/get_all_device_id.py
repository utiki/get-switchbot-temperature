import os
import switchbot_api
import pandas as pd

if __name__ == "__main__":
    devices = switchbot_api.get_all_device_id()
    data = devices['body']['deviceList']
    df = pd.DataFrame(data, columns=['deviceId', 'deviceName', 'deviceType', 'enableCloudService', 'hubDeviceId'])
    print(df.to_string(index=False))
