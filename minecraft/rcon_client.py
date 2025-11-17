"""RCON client for Minecraft server communication."""

from typing import List, Optional
from mcrcon import MCRcon
from utils import (
    get_logger,
    RconConnectionError,
    RconCommandError,
    ServerNotRunningError
)

logger = get_logger(__name__)


class RconClient:
    """Wrapper for Minecraft RCON communication."""
    
    def __init__(self):
        """Initialize RCON client with configuration."""
        # Import the config module directly to get the updated global
        from utils.config import config
        
        self.host = config.server_ip
        self.password = config.rcon_password
        self.port = config.rcon_port
        logger.info(f"RCON client initialized for {self.host}:{self.port}")
    
    def execute(self, command: str) -> str:
        """
        Execute an RCON command.
        
        Args:
            command: The command to execute
            
        Returns:
            Command response from server
            
        Raises:
            RconConnectionError: If connection to server fails
            RconCommandError: If command execution fails
        """
        try:
            logger.debug(f"Executing RCON command: {command}")
            
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                response = mcr.command(command)
                logger.debug(f"RCON response: {response}")
                return response
                
        except ConnectionRefusedError as e:
            logger.error(f"RCON connection refused: {e}")
            raise RconConnectionError(
                "Server is not responding. It may be starting up or shutting down."
            )
        except Exception as e:
            logger.error(f"RCON command failed: {e}")
            raise RconCommandError(command, str(e))
    
    def is_server_running(self) -> bool:
        """
        Check if the server is running and responsive.
        
        Returns:
            True if server is running, False otherwise
        """
        try:
            response = self.execute("list")
            return response.startswith("There are")
        except RconConnectionError:
            return False
        except Exception as e:
            logger.warning(f"Error checking server status: {e}")
            return False
    
    def get_player_list(self) -> List[str]:
        """
        Get list of online players.
        
        Returns:
            List of player names
            
        Raises:
            ServerNotRunningError: If server is not running
        """
        try:
            response = self.execute("list")
            
            if not response.startswith("There are"):
                raise ServerNotRunningError()
            
            # Parse response: "There are X of a max of Y players online: player1, player2"
            if ":" in response:
                players_str = response.split(":", 1)[1].strip()
                if players_str:
                    return [p.strip() for p in players_str.split(",")]
            
            return []
            
        except RconConnectionError:
            raise ServerNotRunningError()
    
    def get_player_count(self) -> int:
        """
        Get the number of online players.
        
        Returns:
            Number of players online
            
        Raises:
            ServerNotRunningError: If server is not running
        """
        players = self.get_player_list()
        return len(players)
    
    def broadcast_message(self, message: str, username: str = "Discord") -> None:
        """
        Broadcast a message to all players.
        
        Args:
            message: Message to send
            username: Username to display (default: "Discord")
            
        Raises:
            ServerNotRunningError: If server is not running
        """
        try:
            # Using tellraw for formatted messages
            json_message = f'{{"text":"[{username}] {message}"}}'
            self.execute(f"tellraw @a {json_message}")
            logger.info(f"Broadcast message from {username}: {message}")
        except RconConnectionError:
            raise ServerNotRunningError()
    
    def stop_server(self) -> None:
        """
        Stop the server gracefully.
        
        Raises:
            ServerNotRunningError: If server is not running
        """
        try:
            logger.info("Sending stop command to server")
            self.execute("stop")
        except RconConnectionError:
            raise ServerNotRunningError()


# Global RCON client instance
rcon_client: Optional[RconClient] = None


def init_rcon() -> RconClient:
    """
    Initialize the global RCON client.
    
    Returns:
        Initialized RconClient instance
    """
    global rcon_client
    rcon_client = RconClient()
    return rcon_client