"""Admin commands for server operators."""

import disnake
from disnake.ext import commands
from minecraft import server_manager, rcon_client
from utils import (
    config,
    get_logger,
    ServerNotRunningError,
    RconConnectionError,
    RconCommandError
)

logger = get_logger(__name__)


class Admin(commands.Cog):
    """Commands for server operators to execute Minecraft commands."""
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the Admin cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        logger.info("Admin cog initialized")
    
    @commands.slash_command(description="Execute a Minecraft command (OP only)")
    async def cmd(
        self,
        inter: disnake.ApplicationCommandInteraction,
        command: str
    ):
        """
        Execute a Minecraft server command via RCON.
        
        This command is restricted to server operators only.
        
        Args:
            inter: The interaction context
            command: The Minecraft command to execute
        """
        await inter.response.defer(ephemeral=True)
        logger.info(f"CMD command invoked by {inter.author} ({inter.author.id}): {command}")
        
        # Check if user is a server operator
        if not config.is_server_op(str(inter.author.id)):
            await inter.edit_original_message(
                content="❌ You don't have permission to use this command.\n"
                        "Only server operators can execute Minecraft commands."
            )
            logger.warning(f"Unauthorized cmd attempt by {inter.author} ({inter.author.id})")
            return
        
        # Check if server is running
        if not server_manager.is_running():
            await inter.edit_original_message(
                content="❌ The server is not running. Please start it with `/start` first."
            )
            return
        
        try:
            # Execute the command via RCON
            response = rcon_client.execute(command)
            
            # Format response
            if response:
                # Truncate long responses
                if len(response) > 1900:
                    response = response[:1900] + "...\n*(Response truncated)*"
                
                await inter.edit_original_message(
                    content=f"**Command:** `{command}`\n**Response:**\n```\n{response}\n```"
                )
            else:
                await inter.edit_original_message(
                    content=f"**Command:** `{command}`\n✅ Command executed (no response)"
                )
            
            logger.info(f"Command executed by {inter.author}: {command}")
            
        except ServerNotRunningError:
            await inter.edit_original_message(
                content="❌ The server is not responding. It may be starting up or shutting down."
            )
        except RconConnectionError:
            await inter.edit_original_message(
                content="❌ Unable to communicate with the server via RCON."
            )
            logger.error("RCON connection failed during cmd execution")
        except RconCommandError as e:
            await inter.edit_original_message(
                content=f"❌ Command execution failed:\n```\n{e.message}\n```"
            )
            logger.error(f"RCON command error: {e}")
        except Exception as e:
            await inter.edit_original_message(
                content="❌ An unexpected error occurred while executing the command."
            )
            logger.error(f"Unexpected error in cmd command: {e}")


def setup(bot: commands.Bot):
    """
    Setup function to add this cog to the bot.
    
    Args:
        bot: The Discord bot instance
    """
    bot.add_cog(Admin(bot))