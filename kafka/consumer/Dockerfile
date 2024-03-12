# Stage 1: Install OpenJDK 11
FROM openjdk:11 AS openjdk_stage

# Stage 2: Build Python with required dependencies
FROM python:3.8 AS python_stage

# Set environment variables for Spark and Hadoop versions
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3.2.2

# Copy JDK from OpenJDK stage
COPY --from=openjdk_stage /usr/local/openjdk-11 /usr/local/openjdk-11

# Set environment variables for Spark and Hadoop paths
ENV JAVA_HOME=/usr/local/openjdk-11
ENV PATH=$JAVA_HOME/bin:$PATH

# Set kafka version
ARG KAFKA_VERSION=2.13-3.7.0
ARG KAFKA_URL=https://dlcdn.apache.org/kafka/3.7.0/kafka_${KAFKA_VERSION}.tgz

# Download and install Spark (assuming downloaded archive is named spark-3.5.1-bin-hadoop3.tgz)
RUN wget -qO- https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz | tar xvz -C /usr/local

# Set environment variables for Spark and Hadoop paths
ENV SPARK_HOME=/usr/local/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=$PATH:${SPARK_HOME}/bin

# Environment variables aws
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

WORKDIR /consumer

COPY consumer.py /consumer

# Install Python dependencies
RUN pip install kafka-python pyspark

# Command to execute the script using spark-submit
CMD ["sh", "-c", "sleep 30 && spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2,com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 consumer.py"]
