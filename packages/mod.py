import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

def get_parent_directory(file_path):
    return os.path.dirname(file_path)

def main_dir(main_script_path):
    parent_directory = get_parent_directory(main_script_path)
    return parent_directory

def flatten(xss):
    return [x for xs in xss for x in xs]

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def current():
    return os.getcwd()

def get_cities(path, country):
    with open(os.path.join(path, "DATA", "city.list.json"), "r") as f:
        data = json.load(f)
    cities = [element["name"] for element in data if element["country"] == country]
    return cities

def read_first_column_csv(path):
    with open(path, "r") as f:
        list2 = [row.split(",")[0] for row in f]
    return list2

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def upload_data(data, key, bucket):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.put_object(Body=data, Bucket=bucket, Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def bardfunc(data):
    columns = []
    values = []
    for key, value in data.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                columns.append(f"{key}/{subkey}")
                values.append(subvalue)
        elif key == "weather":
            for weatherkey, weathervalue in data["weather"][0].items():
                columns.append(f"weather/{weatherkey}")
                values.append(weathervalue)
        else:
            columns.append(key)
            values.append(value)
    return {"columns": columns, "values": values}