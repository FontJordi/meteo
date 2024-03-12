import json
import os
import logging
import boto3
from botocore.exceptions import ClientError
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def get_parent_directory(file_path):
    """
    Returns the parent directory of the given file path.
    """
    return os.path.dirname(file_path)

def main_dir(main_script_path):
    """
    Returns the parent directory of the main script path.
    """
    parent_directory = get_parent_directory(main_script_path)
    return parent_directory

def flatten(xss):
    """
    Flattens a list of lists into a single list.
    """
    return [x for xs in xss for x in xs]

def find_csv_filenames(path_to_dir, suffix=".csv"):
    """
    Finds all filenames with the specified suffix (default is ".csv") in the given directory path.
    """
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def current():
    """
    Returns the current working directory.
    """
    return os.getcwd()

def get_cities(path, country):
    """
    Reads a JSON file containing city data from the specified path and returns a list of city names for the given country.
    """
    with open(os.path.join(path, "DATA", "city.list.json"), "r") as f:
        data = json.load(f)
    cities = [element["name"] for element in data if element["country"] == country]
    return cities

def read_first_column_csv(path):
    """
    Reads the first column of a CSV file and returns it as a list.
    """
    with open(path, "r") as f:
        list2 = [row.split(",")[0] for row in f]
    return list2

def intersection(lst1, lst2):
    """
    Returns the intersection of two lists.
    """
    return [value for value in lst1 if value in lst2]

def upload_data(data, key, bucket):
    """
    Uploads data to an AWS S3 bucket with the specified key using S3 Hook.
    Returns True if the upload is successful, False otherwise.
    """
    s3_hook = S3Hook(aws_conn_id="aws_connection")  # Create S3 Hook with connection ID
    try:
        s3_hook.load_string(string_data=data, key=key, bucket_name=bucket)
    except Exception as e:
        logging.error(e)
        return False
    return True


def bardfunc(data):
    """
    Transforms data into a dictionary containing columns and values, suitable for database insertion.
    Returns a dictionary with keys 'columns' and 'values'.
    """
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