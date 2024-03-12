#!/bin/bash

# Start Zookeeper
#${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties &

# Wait for Zookeeper to start
#sleep 10

# Start Kafka
${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/conf/server-2.properties