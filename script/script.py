import requests
import sys
import time 
import json


sys.path.insert(0, '/home/kiwichi/WEATHERAPI/packages/')

from packages import mod

final_list = mod.intersection(mod.read_first_column_csv("/home/kiwichi/WEATHERAPI/DATA/municipis_catalans.csv"),mod.get_cities("ES"))

with open(mod.current() + "/keys/api.txt","r") as f:
    WEATHER_API_KEY = f.readline()

if __name__ == "__main__":
    country_code = "ES"
    for city in final_list:


        url = "https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_KEY}".format(city_name = city, country_code = "ES", API_KEY = WEATHER_API_KEY)
        res = requests.get(url)
        data = res.json()
        data_string = json.dumps(data,indent=2)

        mod.upload_data(data_string,"meteobucketfirst",country_code,city)
        print(data_string)
        time.sleep(1.5)
