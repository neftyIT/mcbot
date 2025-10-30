"""Server information commands."""

import disnake
from disnake.ext import commands
from minecraft import server_manager, rcon_client
from utils import (
    config,
    get_logger,
    NetworkUtils,
    RconConnectionError
)

logger = get_logger(__name__)


class ServerInfo(commands.Cog):
    """Commands for retrieving server information."""
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the ServerInfo cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.network = NetworkUtils()
        logger.info("ServerInfo cog initialized")
    
    @commands.slash_command(description="Get server information")
    async def info(self, inter: disnake.ApplicationCommandInteraction):
        """
        Display server information and status.
        
        Args:
            inter: The interaction context
        """
        await inter.response.defer()
        logger.info(f"Info command invoked by {inter.author}")
        
        # Build status message
        status_msg = f"**Minecraft Server Information**\n\n"
        status_msg += f"📍 **Server Address:** `{config.server_address}`\n"
        status_msg += f"🔌 **Status:** {'🟢 Running' if server_manager.is_running() else '🔴 Stopped'}\n"
        
        # Get player information if server is running
        if server_manager.is_running():
            try:
                players = rcon_client.get_player_list()
                player_count = len(players)
                
                status_msg += f"👥 **Players Online:** {player_count}\n"
                
                if player_count > 0:
                    player_list = ", ".join(players)
                    status_msg += f"**Players:** {player_list}\n"
                
            except RconConnectionError:
                status_msg += "⚠️ **Note:** Server is starting up or RCON is unavailable\n"
            except Exception as e:
                logger.error(f"Error getting player info: {e}")
                status_msg += "⚠️ **Note:** Unable to fetch player information\n"
        
        await inter.edit_original_message(content=status_msg)
    
    @commands.slash_command(description="Check and update server address")
    async def ipcheck(self, inter: disnake.ApplicationCommandInteraction):
        """
        Check server connectivity and suggest address updates if needed.
        
        Args:
            inter: The interaction context
        """
        await inter.response.defer()
        logger.info(f"IPCheck command invoked by {inter.author}")
        
        # Check if server is running
        if not server_manager.is_running():
            await inter.edit_original_message(
                content="❌ The server is not running. Please start the server first with `/start`."
            )
            return
        
        # Test current address
        host, port = NetworkUtils.validate_address(config.server_address)
        
        if self.network.ping_server(host, port):
            await inter.edit_original_message(
                content=f"✅ Server is reachable at `{config.server_address}`\n\n"
                        f"If you're unable to connect:\n"
                        f"• Check that this address matches what you're using in Minecraft\n"
                        f"• Verify your firewall settings allow port {port}\n"
                        f"• Ensure you're on the same network or have proper port forwarding"
            )
            logger.info(f"Server is reachable at {config.server_address}")
            return
        
        # Current address not working, try external IP
        logger.warning(f"Server not reachable at {config.server_address}, checking external IP")
        
        external_ip = self.network.get_external_ip()
        
        if external_ip:
            external_address = NetworkUtils.format_address(external_ip, port)
            
            # Test external address
            if self.network.ping_server(external_ip, port):
                await inter.edit_original_message(
                    content=f"⚠️ The configured address `{config.server_address}` is not reachable.\n\n"
                            f"✅ However, I detected your external IP. Try using:\n"
                            f"`{external_address}`\n\n"
                            f"**Note:** You may need to update your configuration and restart the bot."
                )
                logger.info(f"External IP {external_address} is reachable")
                return
        
        # Neither worked
        await inter.edit_original_message(
            content=f"❌ Unable to reach the server at `{config.server_address}`"
                    + (f" or external IP `{external_ip}`" if external_ip else "") + "\n\n"
                    f"**Possible issues:**\n"
                    f"• Server is still starting up (wait a few moments)\n"
                    f"• Firewall is blocking connections on port {port}\n"
                    f"• Port forwarding is not configured correctly\n"
                    f"• RCON is not enabled or configured properly\n\n"
                    f"**Troubleshooting:**\n"
                    f"1. Check that `enable-rcon=true` in your server.properties\n"
                    f"2. Verify your firewall allows port {port}\n"
                    f"3. If hosting from home, configure port forwarding on your router\n"
                    f"4. Wait a minute and try `/ipcheck` again"
        )
        logger.error(f"Server not reachable at any tested address")


def setup(bot: commands.Bot):
    """
    Setup function to add this cog to the bot.
    
    Args:
        bot: The Discord bot instance
    """
    bot.add_cog(ServerInfo(bot))