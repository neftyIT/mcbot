# Rewriting the Bot.py from scratch!

## Notes from Nefty

Please note that is my first repo that I am pushing out and I know it is not perfect (as nothing is in life). I had the help of AI tools to help me understand and learn more as I go and also read many documents such as RCON docs, Minecraft Docs, etc... I used Python to create the commands so the code definitely needs more work done to it to make it better as I feel I could have this more cleaner. Please be sure to report any issues or anything that you know or think can help me create this better as I am still learning and growing my developer skills.

### To Do List!

1. Work on bot.py code
2. ADD LICENSE
3. Add Prometheus Installation Script (✅)
4. Add information on how to properly set up Grafana, Prometheus, the Minecraft Node Exporter, and, if needed, Prometheus Node Exporter for node metrics.
5. Fix any small issues that may arise as this gets cloned or forked.

#### Current Tasks
ADD LICENSE TO THIS REPO!!!!!!!!
Add information on how to install Dirien Minecraft Exporter

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
- **Minecraft server**: A running Minecraft server to connect the bot to or you can use the 'server.jar' in the 'newmcworld' directory to create a new world.
- **Discord Bot**: A Discord bot token to manage the server, a Discord server to add the bot to and a channel to type the commands to.

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
    - Add your Discord bot token and Minecraft server details in the `bot.env` file.

4. Start the bot:
    ```bash
    python bot.py
    ```

5. Set up Grafana to visualize metrics of your Minecraft Server (Prometheus, Minecraft Exporter, and any other Grafana tool).
6. Set up Prometheus and add it as a data source to Grafana
7. Set up the Minecraft Exporter and add it to your Prometheus.yml config (For assistance on how to set this up, go here https://github.com/dirien/minecraft-prometheus-exporter?tab=readme-ov-file#getting-started)
8. 

## Monitoring with Grafana

To monitor the Minecraft server, we utilize the following tools:

- **Prometheus**: Collects metrics for visualization on Grafana.
- **Dirien's Minecraft Exporter**: Exports Minecraft server metrics to Prometheus for visualization.

### Grafana Setup

Follow these steps to set up Grafana for monitoring your Minecraft server:

#### 1. **Install Grafana**

We’ve created a script for easy installation and setup of Grafana. The script will install Grafana, configure it, and set up the necessary services. You can find the script in the `/scripts` directory.

To use the script:

1. Navigate to the `scripts` directory

2. Run the script ./grafana_install.sh

3. This script should install Grafana and it's configuration needed. You should be able to find the 'grafana.ini' file in the '/etc/grafana' directory.

4. Grafana runs on port 3000 so ensure your firewall allows the port 3000.

#### 2. **Install Prometheus**

We’ve created a script for easy installation and setup of Prometheus. The script will install Prometheus **and adds the custom configuration needed for Dirien's MC Exporter

1. Navigate to the `scripts` directory

2. Run the script ./prometheus_install.sh

3. This script should install Prometheus and it's configuration needed. You should be able to find the 'prometheus.yml' file in the '/etc/prometheus' directory.

4. Prometheus runs on port 9090 so ensure your firewall allows the port 9090.

#### 3. Setting up the Minecraft Node Exporter for Prometheus

### Minecraft Node Exporter
The Minecraft Node Exporter being used was created by Dirien on Github. Please see below for the link to his repo for the MC Node Exporter for instructions on how to set it up and big thanks from myself as this helped me not have to create a custom node exporter!
[https://github.com/dirien/minecraft-prometheus-exporter]

1. After setting up the MC Exporter, be sure to add the port 9150 to your firewall rules.

2. Access https://localhost:9150/metrics to ensure you metrics from the MC Exporter.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
