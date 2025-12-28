#!/bin/bash

sleep 15 

exec /opt/prometheus/prometheus \
  --config.file=/opt/prometheus/prometheus.yml \
  --storage.tsdb.path=/opt/prometheus/data \
  --web.enable-lifecycle \
  --web.enable-admin-api \
  --web.enable-remote-write-receiver \
  --web.listen-address=:9090 \
  --enable-feature=remote-write-receiver