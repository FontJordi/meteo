import requests
import sys
import datetime
import json
import pandas as pd
import time 
import os

print(str(datetime.datetime.now()))

def set_file_wd():
    os.chdir(os.path.dirname(os.path.abspath(os.path.abspath(__file__))))
    #return os.getcwd()

def move_up_one_level():
    
    os.chdir(os.pardir)
    #return os.getcwd()

def move_down_one_level(dir):
    os.chdir(os.getcwd() + "/" + dir)

set_file_wd()
move_up_one_level()
move_down_one_level("packages")

sys.path.insert(0, os.getcwd())

import mod

set_file_wd()
move_up_one_level()

print(mod.current())

final_list = mod.intersection(mod.read_first_column_csv("/home/kiwichi/WEATHERAPI/DATA/municipis_catalans.csv"),mod.get_cities("ES"))

with open(mod.current() + "/keys/api.txt","r") as f:
    WEATHER_API_KEY = f.readline()

if __name__ == "__main__":

    country_code = "ES"
    columns = ['coord/lon', 'coord/lat', 'weather/id', 'weather/main',
       'weather/description', 'weather/icon', 'base', 'main/temp',
       'main/feels_like', 'main/temp_min', 'main/temp_max', 'main/pressure',
       'main/humidity', 'main/sea_level', 'main/grnd_level', 'visibility',
       'wind/speed', 'wind/deg', 'wind/gust', 'clouds/all', 'dt', 'sys/type',
       'sys/id', 'sys/country', 'sys/sunrise', 'sys/sunset', 'timezone', 'id',
       'name', 'cod']
    
    df = pd.DataFrame(columns=columns)
    
    for city in final_list:

        url = "https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_KEY}".format(city_name = city, country_code = "ES", API_KEY = WEATHER_API_KEY)
        res = requests.get(url)
        data = res.json()
        data_string = json.dumps(data,indent=2)

        df2 = pd.DataFrame(data = [mod.bardfunc(data)["values"]], columns = mod.bardfunc(data)["columns"])
        df = pd.concat([df,df2]).reset_index(drop=True)

        mod.upload_data(data_string,"meteobucketfirst",country_code,city)

        time.sleep(4)

    mod.upload_data(df.to_csv(None),"meteobucketfirst",country = "historical" ,city = str(datetime.datetime.now()) )
    mod.upload_data(df.to_csv(None),"meteobucketfirst",country = "CAT" ,city = "all" )
