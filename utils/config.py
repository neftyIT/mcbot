"""Configuration management for the Minecraft Discord bot."""

import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv
from .exceptions import MissingConfigError, InvalidConfigError


@dataclass
class Config:
    """Bot configuration loaded from environment variables."""
    
    # Discord Configuration
    bot_token: str
    chat_channel_ids: List[int] = field(default_factory=list)
    server_ops: List[str] = field(default_factory=list)
    
    # Minecraft Server Configuration
    server_ip: str = ""
    server_address: str = ""
    server_port: int = 25565
    start_script: str = ""
    
    # RCON Configuration
    rcon_enabled: bool = False
    rcon_password: str = ""
    rcon_port: int = 25575
    
    @classmethod
    def from_env(cls, env_file: str = "bot.env") -> "Config":
        """
        Load configuration from environment file.
        
        Args:
            env_file: Path to the .env file
            
        Returns:
            Config instance with loaded values
            
        Raises:
            MissingConfigError: If required configuration is missing
            InvalidConfigError: If configuration values are invalid
        """
        load_dotenv(dotenv_path=env_file)
        
        # Required fields
        bot_token = os.getenv("bot-token")
        if not bot_token:
            raise MissingConfigError("bot-token")
        
        # Parse server address
        server_address = os.getenv("server-address", "")
        if not server_address:
            raise MissingConfigError("server-address")
        
        # Extract port from address if present
        if ":" in server_address:
            server_ip, port_str = server_address.split(":", 1)
            try:
                server_port = int(port_str)
            except ValueError:
                raise InvalidConfigError("server-address", f"Invalid port number: {port_str}")
        else:
            server_ip = server_address
            server_port = 25565
        
        # Parse chat channel IDs
        chat_channel_id_str = os.getenv("chat-channel-id", "")
        chat_channel_ids = []
        if chat_channel_id_str:
            try:
                chat_channel_ids = [int(id.strip()) for id in chat_channel_id_str.split(",") if id.strip()]
            except ValueError as e:
                raise InvalidConfigError("chat-channel-id", f"Invalid channel ID format: {e}")
        
        # Parse server operators
        server_op_str = os.getenv("server-op", "")
        server_ops = [op.strip() for op in server_op_str.split(",") if op.strip()]
        
        # RCON configuration
        rcon_enabled = os.getenv("enable-rcon", "false").lower() == "true"
        rcon_password = os.getenv("rcon.password", "")
        rcon_port = int(os.getenv("rcon.port", "25575"))
        
        # Start script
        start_script = os.getenv("start-script", "")
        
        return cls(
            bot_token=bot_token,
            chat_channel_ids=chat_channel_ids,
            server_ops=server_ops,
            server_ip=server_ip,
            server_address=server_address,
            server_port=server_port,
            start_script=start_script,
            rcon_enabled=rcon_enabled,
            rcon_password=rcon_password,
            rcon_port=rcon_port,
        )
    
    def validate(self) -> None:
        """
        Validate the configuration.
        
        Raises:
            InvalidConfigError: If configuration is invalid
        """
        if not self.rcon_enabled:
            raise InvalidConfigError(
                "enable-rcon",
                "RCON must be enabled for the bot to function properly"
            )
        
        if not self.rcon_password:
            raise InvalidConfigError(
                "rcon.password",
                "RCON password must be set"
            )
        
        if not self.start_script:
            raise InvalidConfigError(
                "start-script",
                "Start script path must be specified"
            )
        
        if not os.path.isfile(self.start_script):
            raise InvalidConfigError(
                "start-script",
                f"Start script not found at: {self.start_script}"
            )
    
    def is_server_op(self, user_id: str) -> bool:
        """
        Check if a user ID is a server operator.
        
        Args:
            user_id: Discord user ID as string
            
        Returns:
            True if user is a server operator
        """
        return user_id in self.server_ops
    
    def is_chat_channel(self, channel_id: int) -> bool:
        """
        Check if a channel ID is a designated chat channel.
        
        Args:
            channel_id: Discord channel ID
            
        Returns:
            True if channel is a chat channel
        """
        return channel_id in self.chat_channel_ids


# Global config instance (will be initialized in bot.py)
config: Config = None


def init_config(env_file: str = "bot.env") -> Config:
    """
    Initialize the global configuration.
    
    Args:
        env_file: Path to the .env file
        
    Returns:
        Initialized Config instance
    """
    global config
    config = Config.from_env(env_file)
    config.validate()
    return config