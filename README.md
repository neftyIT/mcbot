# IN TESTING STAGE I AM NOT RESPONSILBLE IF YOU CLONE THIS REPO BEFORE I COMPLETE IT

## Notes from Nefty

Please note that is my first repo that I am pushing out and I know it is not perfect (as nothing is in life). I had the help of AI tools to help me understand and learn more as I go. I used Python to create the commands so the code definitely needs more work done to it to make it robust. Please be sure to report any issues or anything that you know or think can help me create this better as I am still learning and growing my developer skills.

### To Do List!

1. Add Prometheus Installation Script ✅ 
2. Add information on how to properly set up Grafana, Prometheus, the Minecraft Node Exporter, and, if needed, Prometheus Node Exporter for node metrics.
3. Fix any small issues that may arise as this gets cloned or forked.

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

## Monitoring with Grafana

To monitor the Minecraft server, we utilize the following tools:

- **Prometheus**: Collects metrics for visualization on Grafana.
- **Minecraft Exporter**: Exports Minecraft server metrics to Prometheus for visualization.

### Grafana Setup

Follow these steps to set up Grafana for monitoring your Minecraft server:

#### 1. **Install Grafana**

We’ve created a script for easy installation and setup of Grafana. The script will install Grafana, configure it, and set up the necessary services. You can find the script in the `/scripts` directory.

To use the script:

1. Navigate to the `scripts` directory

2. Run the script

3. This script should install Grafana and it's configuration needed. You should be able to find the 'grafana.ini' file in the '/etc/grafana' directory.

### Minecraft Node Exporter
The Minecraft Node Exporter being used was created by Dirien on Github. Please see below for the link to his repo for the MC Node Exporter and big thanks from myself as this helped me not have to create a custome node exporter!
[https://github.com/dirien/minecraft-prometheus-exporter]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
