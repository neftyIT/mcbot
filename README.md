# Minecraft Server with Discord Bot Management

This repository contains a Minecraft server setup that is managed using a Discord bot written in Python. The bot allows server management through a variety of commands, and the server's metrics and logs are visualized using Grafana. 

## Commands

The Discord bot currently supports the following commands for managing the Minecraft server:

### 1. `/start`
- **Description**: Starts the Minecraft server.

### 2. `/info`
- **Description**: Retrieves server information, including the server's address.

### 3. `/stop`
- **Description**: Stops the Minecraft server, but only if no players are currently online.

### 4. `/say <message>`
- **Description**: Sends a message in the Minecraft server chat.

### 5. `/ipcheck`
- **Description**: Checks and updates the server address if the one provided in the `/info` command doesn't work.

### 6. `/cmd <command>`
- **Description**: Executes a command directly on the Minecraft server.

## Monitoring with Grafana

To monitor the Minecraft server, we utilize the following tools:

- **Prometheus**: Collects metrics from the server.
- **Loki**: Stores and visualizes logs from the server.
- **Minecraft Exporter**: Exports Minecraft server metrics to Prometheus for visualization.

## Setup

### Prerequisites
- **Minecraft server**: A running Minecraft server to connect the bot to.
- **Discord Bot**: A Discord bot token to manage the server.
- **Grafana**: Installed and configured for monitoring purposes.

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/minecraft-discord-bot.git
    ```

2. Install necessary dependencies:
    ```bash
    cd minecraft-discord-bot
    pip install -r requirements.txt
    ```

3. Configure the bot:
    - Add your Discord bot token and Minecraft server details in the `config.json` file.

4. Start the bot:
    ```bash
    python bot.py
    ```

5. Set up Grafana to visualize metrics and logs (Prometheus, Loki, and Minecraft Exporter).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

