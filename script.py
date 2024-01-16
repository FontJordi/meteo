import requests
from datetime import datetime
import json
import pandas as pd
import time 
import packages.mod as mod


if __name__ == "__main__":


    filenames = mod.find_csv_filenames(mod.current() + "/DATA")
    city_list = []

    for name in filenames:

        city_list.append(mod.intersection(mod.read_first_column_csv(mod.current() + "/DATA/" + name), mod.get_cities("ES")))

    city_list = mod.flatten(city_list)

    with open(mod.current() + "/keys/api.txt","r") as f:
        WEATHER_API_KEY = f.readline()

    country_code = "ES"
    columns = ['coord/lon', 'coord/lat', 'weather/id', 'weather/main',
       'weather/description', 'weather/icon', 'base', 'main/temp',
       'main/feels_like', 'main/temp_min', 'main/temp_max', 'main/pressure',
       'main/humidity', 'main/sea_level', 'main/grnd_level', 'visibility',
       'wind/speed', 'wind/deg', 'wind/gust', 'clouds/all', 'dt', 'sys/type',
       'sys/id', 'sys/country', 'sys/sunrise', 'sys/sunset', 'timezone', 'id',
       'name', 'cod']
    
    #ADD COLUMN message(?)

    df = pd.DataFrame(columns=columns)
    
    for city in city_list:

        url = "https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_KEY}".format(city_name = city, country_code = "ES", API_KEY = WEATHER_API_KEY)
        res = requests.get(url)
        data = res.json()
        data_string = json.dumps(data,indent=2)

        df2 = pd.DataFrame(data = [mod.bardfunc(data)["values"]], columns = mod.bardfunc(data)["columns"])
        df = pd.concat([df,df2]).reset_index(drop=True)

        mod.upload_data(data_string,"meteobucketfirst", country_code, timestamp=datetime.now(), city=city)

        time.sleep(4)

    mod.upload_data(df.to_csv(None, header=False),"meteobucketfirst",country = "ES" ,timestamp = datetime.now(), city='aall' )
