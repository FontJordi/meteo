from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, TimestampType, IntegerType, FloatType, BinaryType, StringType
import pyspark.sql.functions as F
from pyspark.sql.streaming import StreamingQuery
import os
from datetime import datetime

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key_id = os.getenv("AWS_SECRET_ACCESS_KEY")

class KafkaSparkConsumer:
    def __init__(self, kafka_bootstrap_servers, kafka_topic):
        self.spark = SparkSession.builder \
            .appName("KafkaConsumer") \
            .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
            .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key_id) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.endpoint", "s3-eu-west-1.amazonaws.com") \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
            .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
            .getOrCreate()

        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic

        # Define schema for the incoming JSON data
        self.schema = StructType() \
            .add("fakeTimestamp", StringType()) \
            .add("fakeKey", IntegerType()) \
            .add("fakeValue", FloatType())
        
#.add("key", IntegerType()) \
    @staticmethod
    def read_parquet_with_schema(spark, path, schema):
        """
        Read Parquet files with a specified schema.
        """
        return spark.read.schema(schema).parquet(path)
    
    def start_consumer(self):
        # Read data from Kafka topic into a DataFrame
        kafka_df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.kafka_topic) \
            .load()

        kafka_df.printSchema()

        parsed_df = kafka_df.select(
            from_json(col("value").cast("string"), self.schema).alias("data"),
        )
        parsed_df.printSchema()
        # Select the relevant columns from the JSON value
        parsed_df = parsed_df.select(
            col("data.fakeTimestamp").cast("string").alias("timestamp"),
            col("data.fakeKey").cast("integer").alias("key"),
            col("data.fakeValue").cast("float").alias("value")
        )

        # Process the data (replace with your processing logic)


        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        query = parsed_df.writeStream \
            .outputMode("append") \
            .format("csv") \
            .option("path", f"s3a://meteobucketfirst/spark/data/{current_date}") \
            .option("checkpointLocation", f"s3a://meteobucketfirst/spark/metadata/{current_date}") \
            .trigger(processingTime="1 minutes") \
            .start()

        query.awaitTermination()

#postgresql can't insert parquet files directly

if __name__ == "__main__":
    # Define Kafka parameters
    kafka_bootstrap_servers = 'localhost:9092,localhost:9093,localhost:9094'
    kafka_topic = 'my-topic-2'

    # Create an instance of KafkaSparkConsumer
    consumer = KafkaSparkConsumer(kafka_bootstrap_servers, kafka_topic)

    # Start the consumer
    consumer.start_consumer()




#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 consumer.py
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --jars /path/to/hadoop-aws.jar,/path/to/aws-java-sdk.jar consumer.py
#spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.0,com.amazonaws:aws-java-sdk-bundle:1.11.375 consumer.py
#spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.0,com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 consumer.py
#spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2,com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 consumer.py