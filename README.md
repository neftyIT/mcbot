# Minecraft Discord Bot 🎮

**Author:** NEFTY IT  
**Repository:** https://github.com/neftyIT/mcbot/  
**License:** Apache 2.0

A professional Discord bot for managing Minecraft servers with full RCON integration and chat relay features.

## ✨ Features

- **Server Control**: Start and stop your Minecraft server from Discord
- **Chat Integration**: Send messages from Discord to Minecraft
- **Admin Commands**: Execute Minecraft commands via Discord (OP only)
- **Server Monitoring**: Real-time player counts and server status
- **Network Tools**: Automatic IP checking and connectivity diagnostics
- **Clean Architecture**: Modular cog-based design for easy maintenance

## 📋 Requirements

- Python 3.9+
- Minecraft Server (Java Edition) with RCON enabled
- Discord Bot with appropriate permissions

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/neftyIT/mcbot/
cd mcbot
```

### 2. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Minecraft Server

The repository includes a Minecraft server jar in the `world/` directory.
```bash
cd world
java -jar server.jar
```

When prompted, accept the EULA:
```bash
nano eula.txt
# Change eula=false to eula=true
```

Run the server again to generate all files:
```bash
java -jar server.jar
```

Once you see "Done!", stop the server with `stop` command.

### 4. Configure RCON

Edit `world/server.properties`:
```bash
nano server.properties
```

Add or modify these lines:
```properties
enable-rcon=true
rcon.password=your_secure_password
rcon.port=25575
```

### 5. Update Start Script

Edit `world/rconstart.sh` to use the correct path:
```bash
nano rconstart.sh
```

Update the path to your installation:
```bash
#!/bin/bash
cd /absolute/path/to/your/mcbot/world
java -Xmx1024M -Xms1024M -jar server.jar nogui
```

Make it executable:
```bash
chmod +x rconstart.sh
```

### 6. Configure the Bot

Create your environment file:
```bash
cp .env.example .env
nano .env
```

Fill in your configuration:
```env
# Discord Configuration
bot-token=YOUR_DISCORD_BOT_TOKEN
chat-channel-id=YOUR_CHANNEL_ID
server-op=YOUR_DISCORD_USER_ID

# Minecraft Server Configuration
server-address=localhost:25565
start-script=/absolute/path/to/your/mcbot/world/rconstart.sh

# RCON Configuration
enable-rcon=true
rcon.password=your_secure_password
```

**Getting Discord Values:**

1. **bot-token**: 
   - Go to [Discord Developer Portal](https://discord.com/developers/applications/)
   - Create application → Bot → Copy token
   - Enable "Message Content Intent" under Privileged Gateway Intents

2. **chat-channel-id**: 
   - Enable Developer Mode in Discord (User Settings → Advanced)
   - Right-click your channel → Copy ID

3. **server-op**: 
   - Right-click your Discord username → Copy ID

### 7. Run the Bot
```bash
python3 bot.py
```

## 🎮 Commands

### Server Control
- `/start` - Start the Minecraft server
- `/stop` - Stop the server (only if no players online)
- `/info` - Get server status and player information

### Chat
- `/say <message>` - Send a message to Minecraft chat

### Network
- `/ipcheck` - Check server connectivity and get address suggestions

### Admin (OP Only)
- `/cmd <command>` - Execute Minecraft server commands

### Help
- `/help` - Display all available commands

## 📁 Project Structure
```
mcbot/
├── cogs/                   # Discord command modules
│   ├── server_control.py   # Start/stop commands
│   ├── server_info.py      # Info/ipcheck commands
│   ├── chat.py             # Chat relay
│   ├── admin.py            # OP commands
│   └── help.py             # Help command
├── minecraft/              # Minecraft integration
│   ├── rcon_client.py      # RCON wrapper
│   └── server_manager.py   # Process management
├── utils/                  # Utilities
│   ├── config.py           # Configuration
│   ├── logger.py           # Logging setup
│   ├── network.py          # Network utilities
│   └── exceptions.py       # Custom exceptions
├── world/                  # Minecraft server directory
│   ├── server.jar          # Minecraft server
│   └── rconstart.sh        # Start script
├── bot.py                  # Main entry point
└── requirements.txt        # Dependencies
```

## 🔧 Configuration Options

### Discord Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `bot-token` | Your Discord bot token | Yes |
| `chat-channel-id` | Channel IDs for chat relay (comma-separated) | No |
| `server-op` | Discord user IDs with OP permissions (comma-separated) | No |

### Minecraft Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `server-address` | Public server address | Yes |
| `start-script` | Path to server start script | Yes |

### RCON Settings

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `enable-rcon` | Enable RCON | Yes | `true` |
| `rcon.password` | RCON password | Yes | - |
| `rcon.port` | RCON port | No | `25575` |

## 🐛 Troubleshooting

### Server Won't Start
- Check that `start-script` path is correct and absolute
- Verify Java is installed: `java -version`
- Check script permissions: `chmod +x /path/to/rconstart.sh`

### RCON Connection Failed
- Verify `enable-rcon=true` in `server.properties`
- Check RCON password matches in both configs
- Ensure firewall allows RCON port (default 25575)

### Chat Not Working
- Verify `chat-channel-id` is correct
- Bot needs "Manage Webhooks" permission
- Check bot has "Message Content Intent" enabled in Discord Developer Portal

### Commands Not Showing
- Wait a few minutes for Discord to sync commands
- Check bot has "Use Slash Commands" permission
- Try kicking and re-inviting the bot

## 🔒 Security Notes

- **Never commit `.env`** - It contains sensitive tokens
- Use strong RCON passwords
- Restrict OP commands to trusted users only
- Keep dependencies updated for security patches

## 🤝 Contributing

This is a personal project by NEFTY IT. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

Copyright 2025 NEFTY IT

## 🙏 Acknowledgments

Built with:
- [disnake](https://github.com/DisnakeDev/disnake) - Discord API wrapper
- [mcrcon](https://github.com/barneygale/MCRcon) - RCON client library

---

**Made with ❤️ by NEFTY IT**
