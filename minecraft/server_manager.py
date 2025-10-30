"""Minecraft server process management."""

import asyncio
from enum import Enum
from typing import Optional, Callable, Awaitable
from utils import (
    config,
    get_logger,
    ServerNotRunningError,
    ServerAlreadyRunningError,
    ServerStartupError
)

logger = get_logger(__name__)


class ServerState(Enum):
    """Server state enumeration."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"


class ServerManager:
    """Manages the Minecraft server process lifecycle."""
    
    def __init__(self):
        """Initialize the server manager."""
        self.state = ServerState.STOPPED
        self.process: Optional[asyncio.subprocess.Process] = None
        self.output_callback: Optional[Callable[[str], Awaitable[None]]] = None
        self._monitor_task: Optional[asyncio.Task] = None
        logger.info("Server manager initialized")
    
    def is_running(self) -> bool:
        """Check if server is currently running."""
        return self.state == ServerState.RUNNING
    
    def is_stopped(self) -> bool:
        """Check if server is stopped."""
        return self.state == ServerState.STOPPED
    
    def set_output_callback(self, callback: Callable[[str], Awaitable[None]]) -> None:
        """
        Set a callback to handle server output lines.
        
        Args:
            callback: Async function that takes a line string
        """
        self.output_callback = callback
        logger.debug("Output callback registered")
    
    async def start(self) -> None:
        """
        Start the Minecraft server.
        
        Raises:
            ServerAlreadyRunningError: If server is already running
            ServerStartupError: If server fails to start
        """
        if self.state != ServerState.STOPPED:
            raise ServerAlreadyRunningError(f"Server is in state: {self.state.value}")
        
        logger.info(f"Starting Minecraft server with script: {config.start_script}")
        self.state = ServerState.STARTING
        
        try:
            # Start the server process
            self.process = await asyncio.create_subprocess_shell(
                config.start_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            # Start monitoring the output
            self._monitor_task = asyncio.create_task(self._monitor_output())
            
            # Mark as running
            self.state = ServerState.RUNNING
            logger.info("Server started successfully")
            
        except Exception as e:
            self.state = ServerState.STOPPED
            self.process = None
            logger.error(f"Failed to start server: {e}")
            raise ServerStartupError(str(e))
    
    async def stop(self) -> None:
        """
        Stop the Minecraft server.
        
        Note: The actual stop command should be sent via RCON.
        This method waits for the process to terminate.
        
        Raises:
            ServerNotRunningError: If server is not running
        """
        if self.state not in [ServerState.RUNNING, ServerState.STARTING]:
            raise ServerNotRunningError()
        
        logger.info("Stopping server...")
        self.state = ServerState.STOPPING
        
        # The stop command should be sent via RCON by the caller
        # We just wait for the process to exit
        if self.process:
            try:
                # Wait up to 60 seconds for graceful shutdown
                await asyncio.wait_for(self.process.wait(), timeout=60.0)
                logger.info("Server stopped gracefully")
            except asyncio.TimeoutError:
                logger.warning("Server didn't stop gracefully, terminating...")
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    logger.error("Forcing server shutdown")
                    self.process.kill()
                    await self.process.wait()
        
        self.state = ServerState.STOPPED
        self.process = None
        
        # Cancel the monitor task
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Server stopped")
    
    async def _monitor_output(self) -> None:
        """Monitor server output and handle lines."""
        if not self.process or not self.process.stdout:
            return
        
        logger.debug("Starting output monitoring")
        
        try:
            while True:
                line_bytes = await self.process.stdout.readline()
                
                if not line_bytes:
                    # Process ended
                    logger.info("Server process ended")
                    break
                
                # Decode line
                try:
                    line = line_bytes.decode('utf-8').rstrip()
                except UnicodeDecodeError:
                    line = line_bytes.decode('latin-1').rstrip()
                
                # Log the line
                logger.debug(f"Server output: {line}")
                
                # Call callback if set
                if self.output_callback:
                    try:
                        await self.output_callback(line)
                    except Exception as e:
                        logger.error(f"Error in output callback: {e}")
        
        except asyncio.CancelledError:
            logger.debug("Output monitoring cancelled")
            raise
        except Exception as e:
            logger.error(f"Error monitoring output: {e}")
        finally:
            # Mark server as stopped if process ended unexpectedly
            if self.state == ServerState.RUNNING:
                logger.warning("Server process ended unexpectedly")
                self.state = ServerState.STOPPED


# Global server manager instance
server_manager: Optional[ServerManager] = None


def init_server_manager() -> ServerManager:
    """
    Initialize the global server manager.
    
    Returns:
        Initialized ServerManager instance
    """
    global server_manager
    server_manager = ServerManager()
    return server_manager