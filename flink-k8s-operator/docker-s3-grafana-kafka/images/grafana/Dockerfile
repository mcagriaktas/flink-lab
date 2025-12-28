FROM ubuntu:24.04

ENV GRAFANA_VERSION=10.4.14
ENV GRAFANA_HOME=/opt/grafana
ENV ADMIN_USER=
ENV ADMIN_PASSWORD=

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    wget \
    gnupg2 \
    curl \
    jq \
    dos2unix \
    ca-certificates \
    adduser \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key && \
    echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com stable main" > /etc/apt/sources.list.d/grafana.list && \
    apt-get update && \
    apt-get install -y grafana=${GRAFANA_VERSION} && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${GRAFANA_HOME}/plugins \
    ${GRAFANA_HOME}/provisioning/dashboards \
    ${GRAFANA_HOME}/provisioning/dashboards/json \
    ${GRAFANA_HOME}/provisioning/datasources \
    ${GRAFANA_HOME}/data \
    ${GRAFANA_HOME}/logs \
    ${GRAFANA_HOME}/ssl

RUN cp -r /usr/share/grafana/* ${GRAFANA_HOME}/.

WORKDIR ${GRAFANA_HOME}

COPY init-sh/grafana-starter.sh /usr/bin/grafana-starter.sh
RUN chmod +x /usr/bin/grafana-starter.sh

CMD [ "grafana-starter.sh" ]