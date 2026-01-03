# The image is 2.0.1, not 2.0.0!
FROM flink:2.0-scala_2.12

# Flink Application Cluster Env.
ENV FLINK_VERSION=2.0.1
ENV SCALA_VERSION=2.12
ENV FLINK_HOME=/opt/flink
ENV FLINK_LIB=${FLINK_HOME}/lib
ENV FLINK_OPT=${FLINK_HOME}/opt
ENV FLINK_PLUGINS=${FLINK_HOME}/plugins
ENV FLINK_USER_JAR_HOME=${FLINK_HOME}/examples/streaming

# install python3 and pip3
RUN apt-get update -y && \
 apt-get install -y python3 python3-pip python3-dev && \
 rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# Flink S3 Connector
RUN mkdir -p ${FLINK_PLUGINS}/s3-fs-hadoop/ && \
    mv ${FLINK_OPT}/flink-s3-fs-hadoop-2.0.1.jar ${FLINK_PLUGINS}/s3-fs-hadoop/

RUN mv ${FLINK_PLUGINS}/metrics-prometheus/flink-metrics-prometheus-2.0.1.jar ${FLINK_LIB} && \
    rm -rf ${FLINK_PLUGINS}/metrics-prometheus/

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
    
# Flink Kafka Connectors (FLINK 2.0)
RUN wget -q https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/4.0.0-2.0/flink-sql-connector-kafka-4.0.0-2.0.jar -P ${FLINK_LIB} && \
    wget -q https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/4.0.0-2.0/flink-connector-kafka-4.0.0-2.0.jar -P ${FLINK_LIB} && \
    wget -q https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/4.0.0/kafka-clients-4.0.0.jar -P ${FLINK_LIB}

# install PyFlink
RUN pip3 install apache-flink==2.0.1

RUN wget https://github.com/DataSQRL/flink-sql-runner/releases/download/0.9.1/flink-sql-runner-0.9.1-flink-2.2.jar -P ${FLINK_OPT}
COPY flink-sql-runner-1.14.jar ${FLINK_OPT}

# User Own Jar-SQL File
COPY ./FlinkKafkaClient.sql ${FLINK_USER_JAR_HOME}/FlinkKafkaClient.sql