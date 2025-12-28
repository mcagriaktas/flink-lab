FROM ubuntu:22.04

ENV PROMETHEUS_HOME=/opt/prometheus
ENV PROMETHEUS_VERSION=3.5.0

RUN apt-get update && apt-get install -y \
    wget curl \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
    && tar xvfz prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
    && mv prometheus-${PROMETHEUS_VERSION}.linux-amd64 ${PROMETHEUS_HOME} \
    && rm -rf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz prometheus-${PROMETHEUS_VERSION}.linux-amd64

RUN mkdir -p ${PROMETHEUS_HOME}/data ${PROMETHEUS_HOME}/ssl

WORKDIR ${PROMETHEUS_HOME}

COPY init-sh/prometheus-starter.sh /usr/bin/prometheus-starter.sh
RUN chmod +x /usr/bin/prometheus-starter.sh

CMD [ "prometheus-starter.sh" ]