FROM ubuntu:22.04

# Use the version you listed
ENV PUSHGATEWAY_VERSION=1.11.2
ENV PUSHGATEWAY_HOME=/opt/pushgateway

# Install dependencies (wget and ca-certificates are required for HTTPS download)
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create the directory
RUN mkdir -p ${PUSHGATEWAY_HOME}

# Download Pushgateway, extract, and cleanup
RUN wget https://github.com/prometheus/pushgateway/releases/download/v${PUSHGATEWAY_VERSION}/pushgateway-${PUSHGATEWAY_VERSION}.linux-amd64.tar.gz \
    && tar xvfz pushgateway-${PUSHGATEWAY_VERSION}.linux-amd64.tar.gz \
    && cp pushgateway-${PUSHGATEWAY_VERSION}.linux-amd64/pushgateway ${PUSHGATEWAY_HOME}/pushgateway \
    && rm -rf pushgateway-${PUSHGATEWAY_VERSION}.linux-amd64.tar.gz pushgateway-${PUSHGATEWAY_VERSION}.linux-amd64

WORKDIR ${PUSHGATEWAY_HOME}

# Copy your starter script
COPY init-sh/pushgateway-starter.sh /usr/bin/pushgateway-starter.sh
RUN chmod +x /usr/bin/pushgateway-starter.sh

CMD [ "pushgateway-starter.sh" ]