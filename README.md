# Minecraft Discord Bot 🎮

A professional Discord bot for managing Minecraft servers with full RCON integration, monitoring, and chat relay features.

## ✨ Features

- **Server Control**: Start and stop your Minecraft server from Discord
- **Chat Integration**: Bidirectional chat between Discord and Minecraft
- **Admin Commands**: Execute Minecraft commands via Discord (OP only)
- **Server Monitoring**: Real-time player counts and server status
- **Network Tools**: Automatic IP checking and connectivity diagnostics
- **Prometheus Integration**: Export metrics for Grafana dashboards
- **Clean Architecture**: Modular cog-based design for easy maintenance

## 📋 Requirements

- Python 3.9+
- Minecraft Server (Java Edition) with RCON enabled
- Discord Bot with appropriate permissions
- (Optional) Prometheus & Grafana for monitoring

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mcbot.git
cd mcbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and fill in your values:

```bash
cp .env.example bot.env
```

Edit `bot.env`:

```env
# Discord Configuration
bot-token=YOUR_DISCORD_BOT_TOKEN
chat-channel-id=YOUR_CHANNEL_ID
server-op=YOUR_DISCORD_USER_ID

# Minecraft Server Configuration
server-address=YOUR_SERVER_IP:25565
server-ip=YOUR_SERVER_IP
start-script=/path/to/your/rconstart.sh

# RCON Configuration
enable-rcon=true
rcon.password=YOUR_RCON_PASSWORD
rcon.port=25575
```

### 4. Enable RCON on Minecraft Server

Edit your Minecraft server's `server.properties`:

```properties
enable-rcon=true
rcon.password=YOUR_RCON_PASSWORD
rcon.port=25575
```

### 5. Run the Bot

```bash
python bot.py
```

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
├── scripts/                # Installation scripts
│   ├── grafana_install.sh
│   └── prometheus_install.sh
├── bot.py                  # Main entry point
└── requirements.txt        # Dependencies
```

## 🎮 Commands

### Server Control
- `/start` - Start the Minecraft server
- `/stop` - Stop the server (only if no players online)
- `/info` - Get server status and player information

### Chat
- `/say <message>` - Send a message to Minecraft chat
- Messages in designated channels automatically relay to Minecraft

### Network
- `/ipcheck` - Check server connectivity and get address suggestions

### Admin (OP Only)
- `/cmd <command>` - Execute Minecraft server commands

### Help
- `/help` - Display all available commands

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
| `server-ip` | Server IP for RCON | Yes |
| `start-script` | Path to server start script | Yes |

### RCON Settings

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `enable-rcon` | Enable RCON | Yes | `true` |
| `rcon.password` | RCON password | Yes | - |
| `rcon.port` | RCON port | No | `25575` |

## 📊 Monitoring Setup

### Prometheus

Install Prometheus using the provided script:

```bash
cd scripts
sudo ./prometheus_install.sh
```

### Grafana

Install Grafana:

```bash
cd scripts
sudo ./grafana_install.sh
```

### Minecraft Exporter

1. Copy the exporter files:
```bash
sudo cp config/minecraft_exporter/minecraft-exporter /usr/local/bin/
sudo cp config/minecraft_exporter/minecraft-exporter.service /etc/systemd/system/
```

2. Enable and start:
```bash
sudo systemctl enable minecraft-exporter
sudo systemctl start minecraft-exporter
```

3. Configure firewall:
```bash
sudo ufw allow 9150/tcp
```

## 🐛 Troubleshooting

### Server Won't Start
- Check that `start-script` path is correct
- Verify Java is installed: `java -version`
- Check script permissions: `chmod +x /path/to/rconstart.sh`

### RCON Connection Failed
- Verify `enable-rcon=true` in `server.properties`
- Check RCON password matches in both configs
- Ensure firewall allows RCON port (default 25575)

### Chat Not Working
- Verify `chat-channel-id` is correct
- Bot needs "Manage Webhooks" permission
- Check bot has "Message Content Intent" enabled

### Commands Not Showing
- Wait a few minutes for Discord to sync commands
- Check bot has "Use Slash Commands" permission
- Try kicking and re-inviting the bot

## 🔒 Security Notes

- **Never commit `bot.env`** - It contains sensitive tokens
- Use strong RCON passwords
- Restrict OP commands to trusted users only
- Keep dependencies updated for security patches

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [disnake](https://github.com/DisnakeDev/disnake) - Discord API wrapper
- [mcrcon](https://github.com/barneygale/MCRcon) - RCON client library
- [Dirien's Minecraft Exporter](https://github.com/dirien/minecraft-prometheus-exporter) - Prometheus metrics

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Join our Discord community (link)

---

**Note**: This is a refactored and improved version of the original bot with better structure, error handling, and maintainability.