#!/bin/bash

sudo apt -y install prometheus prometheus-node-exporter

# Path to Prometheus configuration file
PROMETHEUS_CONFIG="/etc/prometheus/prometheus.yml"

# Check if Prometheus config file exists
if [[ ! -f "$PROMETHEUS_CONFIG" ]]; then
    echo "Prometheus configuration file not found at $PROMETHEUS_CONFIG"
    exit 1
fi

# Add Minecraft Exporter scrape config
echo "Adding Minecraft Node Exporter configuration to Prometheus..."

cat <<EOF >> "$PROMETHEUS_CONFIG"

  - job_name: 'Minecraft-Node-Exporter'
    static_configs:
      - targets: ['localhost:9150']
EOF

echo "Minecraft Node Exporter configuration added successfully."

# Restart Prometheus to apply changes
echo "Restarting Prometheus service..."
sudo systemctl restart prometheus

if [[ $? -eq 0 ]]; then
    echo "Prometheus restarted successfully."
else
    echo "Failed to restart Prometheus. Please check the service status."
fi
