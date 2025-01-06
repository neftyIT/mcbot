#!/bin/bash

# Variables
GRAFANA_REPO="deb https://packages.grafana.com/oss/deb stable main"
GRAFANA_GPG_KEY_URL="https://packages.grafana.com/gpg.key"
SERVICE_FILE="/etc/systemd/system/grafana-server.service"

# Add the Grafana APT repository:
echo "Adding Grafana APT repository..."
sudo add-apt-repository "$GRAFANA_REPO"

# Add the Grafana GPG key:
echo "Adding Grafana GPG key..."
sudo wget -q -O - "$GRAFANA_GPG_KEY_URL" | sudo apt-key add -

# Update the package list:
echo "Updating package list..."
sudo apt-get update

# Install Grafana:
echo "Installing Grafana..."
sudo apt-get install -y grafana

# Stop Grafana service (if it's running)
echo "Stopping Grafana service..."
sudo systemctl stop grafana-server

# Update the Grafana service file
echo "Updating the Grafana service file..."
sudo bash -c "cat > $SERVICE_FILE << EOF
[Unit]
Description=Grafana instance
Documentation=http://docs.grafana.org
Wants=network-online.target
After=network-online.target

[Service]
EnvironmentFile=-/etc/default/grafana-server
User=grafana
Group=grafana
Type=simple
ExecStart=/usr/sbin/grafana-server --config=/etc/grafana/grafana.ini \
--homepath=/usr/share/grafana \
cfg:default.paths.logs=/var/log/grafana \
cfg:default.paths.data=/var/lib/grafana \
cfg:default.paths.plugins=/var/lib/grafana/plugins
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF"

# Reload the systemd service manager
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start the Grafana service
echo "Enabling and starting the Grafana service..."
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

echo "Grafana installation and configuration complete."
