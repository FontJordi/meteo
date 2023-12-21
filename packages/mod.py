import json
import csv 
import requests
import os
import logging
import boto3
from botocore.exceptions import ClientError
import os


def current():
    return os.getcwd()

def parent(path):
    path = os.getcwd()
    return os.path.abspath(os.path.join(path, os.pardir))

def get_cities(country):

    with open("/home/kiwichi/WEATHERAPI/DATA/city.list.json", "r") as f:
        data = json.load(f)
    cities = []

    for element in data:
        if element["country"] == country:
            cities.append(element["name"])
            #print(element["name"])

    return cities

def read_first_column_csv(path):

    list2 = []

    with open(path,"r") as f:
        for row in f:
            list2.append(row.split(",")[0])

    return(list2)

#print(read_first_column_csv("/home/kiwichi/WEATHERAPI/DATA/municipis_catalans.csv"))
#print(get_cities("ES"))

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def upload_data(data, bucket, country,city):

    key = "{country}/{city}".format(country=country, city=city)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.put_object(Body=data,Bucket=bucket,Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True
