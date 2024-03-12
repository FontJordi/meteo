FROM openjdk:8-jdk-alpine

# Set kafka version
ARG KAFKA_VERSION=2.13-3.7.0
ARG KAFKA_URL=https://dlcdn.apache.org/kafka/3.7.0/kafka_${KAFKA_VERSION}.tgz

# Install required packages
RUN apk update && \
    apk add --no-cache bash curl tar jq

# Download and extract Kafka
RUN wget -qO /tmp/kafka.tgz ${KAFKA_URL} \
    && tar -xzf /tmp/kafka.tgz -C /opt \
    && rm /tmp/kafka.tgz

# Set Kafka home environment variable
ENV KAFKA_HOME /opt/kafka_${KAFKA_VERSION}

# Expose Kafka port
#EXPOSE 9093

# Copy startup script
COPY server-start.sh /

# Create logs folder
WORKDIR /opt/kafka_${KAFKA_VERSION}
RUN mkdir logsdir

# Copy server properties
WORKDIR /opt/kafka_${KAFKA_VERSION}/config
RUN mkdir conf 
COPY server-1.properties conf/

# Set permissions for the startup script
RUN chmod +x /server-start.sh

# Start Zookeeper and Kafka servers
CMD ["/server-start.sh"]