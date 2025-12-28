#!/bin/bash

sleep 15

/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic $SOURCE_TOPIC \
  --replication-factor 3 \
  --partitions 12

/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic $SINK_TOPIC \
  --replication-factor 3 \
  --partitions 12

/opt/kafka/bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name $SOURCE_TOPIC \
  --alter --add-config max.message.bytes=15728640

/opt/kafka/bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name $SINK_TOPIC \
  --alter --add-config max.message.bytes=15728640