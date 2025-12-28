#!/bin/bash
set -e

echo "Starting Pushgateway..."

# Run the binary
# --web.listen-address=":9091" ensures it listens on the correct port
exec /opt/pushgateway/pushgateway --web.listen-address=":9091"