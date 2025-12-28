#!/usr/bin/env bash
set -Eeuo pipefail

echo "Starting Grafana initialization..."

GRAFANA_HOME="/opt/grafana"
OUT_DIR="$GRAFANA_HOME/provisioning/datasources"
OUT_FILE="$OUT_DIR/datasource.yaml"
GRAFANA_CFG="${GRAFANA_HOME}/confs/grafana.ini"

if [[ -n "${ADMIN_PASSWORD_FILE:-}" && -f "${ADMIN_PASSWORD_FILE}" ]]; then
  ADMIN_PASSWORD="$(<"$ADMIN_PASSWORD_FILE")"
fi
: "${ADMIN_USER:=cagri}"
: "${ADMIN_PASSWORD:=3541}"

mkdir -p "$OUT_DIR" "$GRAFANA_HOME/data" "$GRAFANA_HOME/logs" "$GRAFANA_HOME/provisioning" \
  "$GRAFANA_HOME/provisioning/alerting" "$GRAFANA_HOME/provisioning/notifiers" "$GRAFANA_HOME/provisioning/plugins"

export GF_SECURITY_ADMIN_USER="$ADMIN_USER"
export GF_SECURITY_ADMIN_PASSWORD="$ADMIN_PASSWORD"
export GF_PATHS_DATA="$GRAFANA_HOME/data"
export GF_PATHS_LOGS="$GRAFANA_HOME/logs"
export GF_PATHS_PROVISIONING="$GRAFANA_HOME/provisioning"

GRAFANA_BIN="$GRAFANA_HOME/bin/grafana-server"
echo "Datasource rendered -> $OUT_FILE"
echo "Starting Grafana..."
exec "$GRAFANA_BIN" \
  --homepath="$GRAFANA_HOME" \
  --config="$GRAFANA_CFG" \
  "$@"