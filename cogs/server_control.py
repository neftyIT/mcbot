"""Server control commands (start/stop)."""

import disnake
from disnake.ext import commands
from minecraft import server_manager, rcon_client
from utils import (
    get_logger,
    ServerAlreadyRunningError,
    ServerNotRunningError,
    ServerStartupError,
    RconConnectionError
)

logger = get_logger(__name__)


class ServerControl(commands.Cog):
    """Commands for starting and stopping the Minecraft server."""
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the ServerControl cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        logger.info("ServerControl cog initialized")
    
    @commands.slash_command(description="Starts the Minecraft server")
    async def start(self, inter: disnake.ApplicationCommandInteraction):
        """
        Start the Minecraft server.
        
        Args:
            inter: The interaction context
        """
        await inter.response.defer()
        logger.info(f"Start command invoked by {inter.author}")
        
        try:
            if server_manager.is_running():
                await inter.edit_original_message(
                    content="❌ The server is already running!"
                )
                return
            
            # Start the server
            await server_manager.start()
            
            await inter.edit_original_message(
                content="✅ Server started successfully! It may take a few moments to fully initialize."
            )
            logger.info("Server started via Discord command")
            
        except ServerAlreadyRunningError:
            await inter.edit_original_message(
                content="❌ The server is already running!"
            )
        except ServerStartupError as e:
            await inter.edit_original_message(
                content=f"❌ Failed to start the server: {e.message}"
            )
            logger.error(f"Failed to start server: {e}")
        except Exception as e:
            await inter.edit_original_message(
                content="❌ An unexpected error occurred while starting the server."
            )
            logger.error(f"Unexpected error starting server: {e}")
    
    @commands.slash_command(description="Stops the Minecraft server")
    async def stop(self, inter: disnake.ApplicationCommandInteraction):
        """
        Stop the Minecraft server (only if no players are online).
        
        Args:
            inter: The interaction context
        """
        await inter.response.defer()
        logger.info(f"Stop command invoked by {inter.author}")
        
        try:
            if not server_manager.is_running():
                await inter.edit_original_message(
                    content="❌ The server is not running."
                )
                return
            
            # Check if players are online
            try:
                player_count = rcon_client.get_player_count()
                
                if player_count > 0:
                    players = rcon_client.get_player_list()
                    player_list = ", ".join(players)
                    await inter.edit_original_message(
                        content=f"❌ Cannot stop the server while players are online!\n"
                                f"**Online players ({player_count}):** {player_list}"
                    )
                    return
            except RconConnectionError:
                # Server might be in transition state
                await inter.edit_original_message(
                    content="⚠️ Unable to check player count. The server may be starting up or shutting down."
                )
                return
            
            # Send stop command via RCON
            rcon_client.stop_server()
            
            # Wait for server to stop
            await server_manager.stop()
            
            await inter.edit_original_message(
                content="✅ Server stopped successfully."
            )
            logger.info("Server stopped via Discord command")
            
        except ServerNotRunningError:
            await inter.edit_original_message(
                content="❌ The server is not running."
            )
        except RconConnectionError:
            await inter.edit_original_message(
                content="❌ Unable to communicate with the server."
            )
            logger.error("RCON connection failed during stop command")
        except Exception as e:
            await inter.edit_original_message(
                content="❌ An unexpected error occurred while stopping the server."
            )
            logger.error(f"Unexpected error stopping server: {e}")


def setup(bot: commands.Bot):
    """
    Setup function to add this cog to the bot.
    
    Args:
        bot: The Discord bot instance
    """
    bot.add_cog(ServerControl(bot))