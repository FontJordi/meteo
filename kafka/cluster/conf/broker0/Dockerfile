FROM python:3.8

# Install Java JDK 11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set kafka version
ARG KAFKA_VERSION=2.13-3.7.0
ARG KAFKA_URL=https://dlcdn.apache.org/kafka/3.7.0/kafka_${KAFKA_VERSION}.tgz

# Download and install kafka
RUN wget -qO /tmp/kafka.tgz ${KAFKA_URL} \
    && tar -xzf /tmp/kafka.tgz -C /opt \
    && rm /tmp/kafka.tgz

# Create logs directory for the 3 different brokers
RUN /opt/kafka_${KAFKA_VERSION}/logsdir1 && \
    /opt/kafka_${KAFKA_VERSION}/logsdir2 && \
    /opt/kafka_${KAFKA_VERSION}/logsdir3

# Set working directory
WORKDIR /opt/kafka_${KAFKA_VERSION}/config
RUN mkdir conf 
COPY conf/server.properties conf/
COPY conf/server-1.properties conf/
COPY conf/server-2.properties conf/

EXPOSE 9092 9093 9094

CMD ["bin/kafka-topics.sh --create --topic my-topic-2 --bootstrap-server localhost:9092"]
CMD ["/opt/kafka_${KAFKA_VERSION}/bin/kafka-server-start.sh", "/opt/kafka_${KAFKA_VERSION}/bin/kafka-server-start.sh", "/opt/kafka_${KAFKA_VERSION}/config/conf/server-1.properties", "/opt/kafka_${KAFKA_VERSION}/config/conf/server-2.properties"]
