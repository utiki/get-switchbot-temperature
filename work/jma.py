import requests

def get_northwest_chiba_weather():
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    wether = None
    for area in data[0]["timeSeries"][0]["areas"]:
        if area["area"]["name"] == "北西部":
            wether = area["weathers"][0]
            break
    return wether

if __name__ == "__main__":
    print(get_northwest_chiba_weather())