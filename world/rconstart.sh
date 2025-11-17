#!/bin/bash
cd ~/mcbot/world
java -Xmx1024M -Xms1024M -jar server.jar nogui 
echo "Minecraft server started in nogui mode. Logs are saved in server.log."
