#!/bin/bash
cd ~/Projects/mcbot/newmcworld
java -Xmx1024M -Xms1024M -jar minecraft_server.1.21.4.jar nogui >> server.log 2>&1 &
echo "Minecraft server started in nogui mode. Logs are saved in server.log."
