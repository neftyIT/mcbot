# Notes from Nefty
Please note that is my first repo that I am pushing out and I know it is not perfect (as nothing is in life). I had the help of AI tools to help me understand and learn more as I go and also read documents such as RCON docs, Minecraft Docs, and more. I used Python to create the commands so the code definitely needs more work done to it to make it better as I feel I could have this more cleaner. Please be sure to report any issues or anything that you know or think can help me create this better as I am still learning and growing my developer skills. **REPO STILL IN TESTING STAGE USE AT YOUR OWN DISCRETION**

# Notes for the bot
Currently when you use the command '/start' this will start the server but if you stop the bot, the Minecraft world itself will stop as well. This is something I need to work on with the bot.py code.

## To Do List!

1. Work on bot.py code to make it cleaner
2. Create a custom dashboard on Grafana for the MC Node Exporter

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
- **Java OpenJDK 21**: Currently we are using Java 21 to run the Minecraft server for now.

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
    python3 bot.py
    ```

5. Set up Grafana to visualize metrics of your Minecraft Server (Prometheus, Minecraft Exporter, and any other Grafana tool).
6. Set up Prometheus and add it as a data source to Grafana
7. Set up the Minecraft Exporter and add it to your Prometheus.yml config (For assistance on how to set this up, go here https://github.com/dirien/minecraft-prometheus-exporter?tab=readme-ov-file#getting-started)

## Monitoring with Grafana

To monitor the Minecraft server, we utilize the following tools:

- **Prometheus**: Collects metrics for visualization on Grafana.
- **Dirien's Minecraft Exporter**: Exports Minecraft server metrics to Prometheus for visualization.

## Grafana Setup

Follow these steps to set up Grafana for monitoring your Minecraft server:

### 1. **Install Grafana**

We’ve created a script for easy installation and setup of Grafana. The script will install Grafana, configure it, and set up the necessary services. You can find the script in the `/scripts` directory.

To use the script:

1. Navigate to the `scripts` directory

2. Run the script ./grafana_install.sh

3. This script should install Grafana and it's configuration needed. You should be able to find the 'grafana.ini' file in the '/etc/grafana' directory.

4. Grafana runs on port 3000 so ensure your firewall allows the port 3000.

## Prometheus and Prometheus Node Exporter Setup

### 2. **Install Prometheus**

We’ve created a script for easy installation and setup of Prometheus and Prometheus Node Exporter. The script will install Prometheus **and adds the custom configuration needed for Dirien's MC Exporter

1. Navigate to the `scripts` directory

2. Run the script with **sudo** ./prometheus_install.sh. This allows for the MC Exporter configuration to be added to the prometheus.yml

3. This script should install Prometheus and it's configuration needed. You should be able to find the 'prometheus.yml' file in the '/etc/prometheus' directory.

4. Prometheus runs on port 9090 so ensure your firewall allows the port 9090.

5. The Prometheus Node Exporter is included in the script. Be sure to run **sudo systemctl status prometheus-node-exporter** to verify that it was installed and is running.

6. You can go to http://localhost:9090/ which should direct you to the Prometheus web interface.

### Dirien's Minecraft Exporter

## 3. Setting up the Minecraft Node Exporter for Prometheus

### Minecraft Node Exporter
The Minecraft Node Exporter being used in this repo was created by Dirien on Github. Please see below for the link to his repo for the MC Node Exporter to take a further look at his repo.
[https://github.com/dirien/minecraft-prometheus-exporter]

1. I've included the MC Exporter and the Systemd Unit File in the config/minecraft_exporter directory so you will need to do the following:
     cp minecraft-exporter /usr/local/bin
     cp minecraft-exporter.service /etc/systemd/system
  
2. After setting up the MC Exporter, be sure to add the port 9150 to your firewall rules.

3. Access https://localhost:9150/metrics to ensure you can see metrics from the MC Exporter.

## Discord McBot

### 4. Setting up the Discord McBot

1. Create a Discord Developer account and create an application.

2. Copy your Token key from the Bot tab and then head to OAuth2

3. In the OAuth2 page, scroll down OAuth2 URL Generator and click the following: \
         Scope: Bot \   
           Bot Permissions:   Manage Messages and Use Slash Commands 

4. Once this is completed, copy the URL and invite your bot to your Discord Server

5. Create a channel on Discord and copy the channel ID.

6. Go to the bot.env and fill out the variables:

    e.g
    
    bot-token=thisis4examplew1lln0tw0rk \
    server-address=192.168.230.67:25565 \
    start-script=home/*user*/mcbot/rconstart.sh \
    server-ip=192.168.230.67 \
    server-op=Himothy \
    chat-channel-id=1328407534503067688 \
    #enable-rcon & rcon.port should stay the same unless you like customizing \
    enable-rcon=true \
    rcon.password=wh@t1s@p@ssw0rd \
    rcon.port=25575

7. After entering you environmental variables, start the bot using 'python3 (or just python) bot.py'. 

8. You should see the bot online in discord and you should be able to use commmands.

9. Ensure that you have the setting 'enable-rcon=**true**' in the server.properties of your Minecraft world as the default is set to **false**

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
