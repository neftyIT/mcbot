# Minecraft Server with Discord Bot Management

This repository contains a Minecraft server setup that is managed using a Discord bot written in Python. The bot allows server management through a variety of commands, and the server's metrics and logs are visualized using Grafana.

## Commands

The Discord bot currently supports the following commands for managing the Minecraft server:

1. **/start**  
   *Description*: Starts the Minecraft server.

2. **/info**  
   *Description*: Retrieves server information, including the server's address.

3. **/stop**  
   *Description*: Stops the Minecraft server, but only if no players are currently online.

4. **/say <message>**  
   *Description*: Sends a message in the Minecraft server chat.

5. **/ipcheck**  
   *Description*: Checks and updates the server address if the one provided in the /info command doesn't work.

6. **/cmd <command>**  
   *Description*: Executes a command directly on the Minecraft server.

## Setup

### Prerequisites
- **Minecraft server**: A running Minecraft server to connect the bot to.
- **Discord Bot**: A Discord bot token to manage the server.
- **Grafana**: Installed and configured for monitoring purposes.

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/neftyIT/mcbot.git
    ```

2. Install necessary dependencies:
    ```bash
    cd mcbot
    pip install -r requirements.txt
    ```

3. Configure the bot:
    - Add your Discord bot token and Minecraft server details in the `config.json` file.

4. Start the bot:
    ```bash
    python bot.py
    ```

5. Set up Grafana to visualize metrics and logs (Prometheus, Loki, Minecraft Exporter, and any other Grafana tool).

## Monitoring with Grafana

To monitor the Minecraft server, we utilize the following tools:

- **Prometheus**: Collects metrics from the server.
- **Loki**: Stores and visualizes logs from the server.
- **Minecraft Exporter**: Exports Minecraft server metrics to Prometheus for visualization.

### Grafana Setup

Follow these steps to set up Grafana for monitoring your Minecraft server:

#### 1. **Install Grafana**

We’ve created a script for easy installation and setup of Grafana. The script will install Grafana, configure it, and set up the necessary services. You can find the script in the `/scripts` directory.

To use the script:

1. Navigate to the `scripts` directory

2. Edit the grafana_install.sh script to customize the directory path and other configurations as per your requirements.

3.Run the script

4. This script does the following:

Installs Grafana.
Configures Grafana with custom settings (including the grafana.ini file).
Updates the Grafana service file to point to the custom configuration.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Changes:
- **Grafana Installation Script**: Moved the full installation script to the `/scripts` directory, with instructions to customize the script before running it.
- **Note for Customization**: Mentioned that users should edit the `grafana_install.sh` script to customize the directory and other paths as needed.

Now, users can easily locate the script in the `/scripts` folder and modify it according to their setup before running it. Let me know if you need further modifications!
