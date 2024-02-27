import json
import pandas as pd
import requests
import time
from datetime import datetime
from packages import mod

def fetch_weather_data(city_list, country_code, api_key):
    columns = ['coord/lon', 'coord/lat', 'weather/id', 'weather/main',
               'weather/description', 'weather/icon', 'base', 'main/temp',
               'main/feels_like', 'main/temp_min', 'main/temp_max', 'main/pressure',
               'main/humidity', 'main/sea_level', 'main/grnd_level', 'visibility',
               'wind/speed', 'wind/deg', 'wind/gust', 'clouds/all', 'dt', 'sys/type',
               'sys/id', 'sys/country', 'sys/sunrise', 'sys/sunset', 'timezone', 'id',
               'name', 'cod', 'rain/1h', 'rain/3h', 'snow/1h', 'snow/3h', 'insertdatetime']

    df = pd.DataFrame(columns=columns)
    json_list = []

    for city in city_list:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}"
        res = requests.get(url)
        data = res.json()
        data['insertdatetime'] = datetime.now().isoformat()
        data_string = json.dumps(data, indent=2)
        json_list.append(data)
        df2 = pd.DataFrame(data=[mod.bardfunc(data)["values"]],
                           columns=mod.intersection(mod.bardfunc(data)["columns"], columns))
        df = pd.concat([df, df2]).reset_index(drop=True)
        print(df)
        time.sleep(3.5)

    return df, json_list

def main():
    api_key_path = mod.main_dir(__file__) + "/keys/api.txt"
    with open(api_key_path, "r") as f:
        weather_api_key = f.readline()

    country_code = "ES"
    csv_filenames = mod.find_csv_filenames(mod.main_dir(__file__) + "/DATA")
    city_list = []
    for name in csv_filenames:
        city_list.append(mod.intersection(mod.read_first_column_csv(mod.main_dir(__file__) + "/DATA/" + name),
                                          mod.get_cities(mod.main_dir(__file__), country_code)))

    city_list = mod.flatten(city_list)

    df, json_list = fetch_weather_data(city_list, country_code, weather_api_key)

    # Uncomment below to upload data
    # mod.upload_data(json_list, "meteobucketfirst", country_code, timestamp=datetime.now())
    mod.upload_data(df.to_csv(None, header=False, index=False),
                    f"historical/meteo/{country_code}/{datetime.now()}",
                    "meteobucketfirst")

if __name__ == "__main__":
    main()