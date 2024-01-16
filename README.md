This is a personal project made with the intentions to learn 

notes: current etl working. have to work on:

imports on scrpit.py
upload terraform to github
upload airflow dags
dockerize everything
code airflow connections and rds permissions to access bucket (maybe user too?) assign role to rds.
parametrize uploads to s3 (country)

How to use:

city.list.json is a downloaded json file from openweaterapi containing all the cities available

there has to be a folder keys with an api.txt file containing you openweatherapi key

in DATA/ there has to be csv files where the first column has the name of the cities you want to take into account