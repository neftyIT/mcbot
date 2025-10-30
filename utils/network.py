"""Network utilities for server connectivity checks."""

import socket
import urllib.request
from typing import Tuple, Optional
from .logger import get_logger
from .exceptions import ServerUnreachableError

logger = get_logger(__name__)


class NetworkUtils:
    """Utilities for network connectivity checks."""
    
    @staticmethod
    def ping_server(host: str, port: int, timeout: int = 5) -> bool:
        """
        Check if a server is reachable.
        
        Args:
            host: Server hostname or IP
            port: Server port
            timeout: Connection timeout in seconds
            
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.debug(f"Server reachable at {host}:{port}")
                return True
            else:
                logger.debug(f"Server unreachable at {host}:{port} (error code: {result})")
                return False
                
        except socket.gaierror as e:
            logger.error(f"Failed to resolve hostname {host}: {e}")
            return False
        except socket.timeout:
            logger.error(f"Connection timeout for {host}:{port}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during ping to {host}:{port}: {e}")
            return False
    
    @staticmethod
    def get_external_ip() -> Optional[str]:
        """
        Get the external IP address of this machine.
        
        Returns:
            External IP address as string, or None if unable to determine
        """
        try:
            response = urllib.request.urlopen('https://ident.me', timeout=5)
            external_ip = response.read().decode('utf8')
            logger.info(f"External IP detected: {external_ip}")
            return external_ip
        except Exception as e:
            logger.error(f"Failed to get external IP: {e}")
            return None
    
    @staticmethod
    def validate_address(address: str) -> Tuple[str, int]:
        """
        Validate and parse a server address.
        
        Args:
            address: Server address in format "host:port" or "host"
            
        Returns:
            Tuple of (host, port)
            
        Raises:
            ValueError: If address format is invalid
        """
        if ":" in address:
            parts = address.split(":", 1)
            host = parts[0]
            try:
                port = int(parts[1])
                if not (1 <= port <= 65535):
                    raise ValueError(f"Port must be between 1 and 65535, got {port}")
            except ValueError as e:
                raise ValueError(f"Invalid port in address '{address}': {e}")
        else:
            host = address
            port = 25565  # Default Minecraft port
        
        if not host:
            raise ValueError("Host cannot be empty")
        
        return host, port
    
    @staticmethod
    def format_address(host: str, port: int) -> str:
        """
        Format a host and port into an address string.
        
        Args:
            host: Server hostname or IP
            port: Server port
            
        Returns:
            Formatted address string
        """
        if port == 25565:
            return host
        return f"{host}:{port}"