import csv
import requests
import packages.mod as mod
from datetime import datetime

url_air_quality = 'https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.csv'
url_radiation = 'tps://analisi.transparenciacatalunya.cat/resource/wpez-cjrc.csv'

with requests.Session() as s:
    air_quality = s.get(url_air_quality )
    radiation = s.get(url_radiation)

    #decoded_content = air_quality.content.decode('utf-8')
    #decoded_content = url_radiation.content.decode('utf-8')

    mod.upload_data(air_quality.content,
                    "historical/air_quality/" + str(datetime.now()),
                    "meteobucketfirst")

    mod.upload_data(radiation,
                    "historical/radiation/" + str(datetime.now()),
                    "meteobucketfirst")
