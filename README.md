## Description

### Objective
This project will show current and historical data from towns in Catalonia. It will also make up data to send it through Kafka (this way I can send as much data as I want, without worrying about API limits). 

I approached the project more from a learning experience, rather than a practical one. The objective of this project is to implement various technologies to gain an understanding of how they work and the advantages and disadvantages of each one.

### Dataset

[OpenWeatherMap](https://openweathermap.org/) is an API which collects meteorological data ffrom around the globe, and [Generalitat de Catalunya](https://analisi.transparenciacatalunya.cat/), a public data collection of the government of catalonia.

### Tools & Technologies

- Cloud - [**Amazon Web Services**](https://aws.amazon.com/)
- Infrastructure as Code software - [**Terraform**](https://www.terraform.io)
- Orchestration - [**Airflow**](https://airflow.apache.org)
- Transformation - [**dbt**](https://www.getdbt.com)
- Data Lake - [**Amazon S3**](https://aws.amazon.com/es/s3/)
- Data Warehouse - [**Amazon RDS (PostgreSQL)**](https://aws.amazon.com/free/database/)
- Data Visualization - [**Metabase**](https://www.metabase.com/)
- Language - [**Python**](https://www.python.org)
- Streaming processing - [**Kafka**](https://kafka.apache.org/), [**SparkStreaming**](https://spark.apache.org/)

### Architecture

![streamify-architecture](images/catetl.png)


### Pre-requisites

- Amazon Web Services account
- OpenWeatherMap API account

## Setup

 - Setup Airflow
 - Setup dbt envoirment
 - Setup Kafka
 - Launch terraform template
 - Setup Metabase

# WORK IN PROGRESS
