"""Help command and bot information."""

import disnake
from disnake.ext import commands
from utils import get_logger

logger = get_logger(__name__)


class Help(commands.Cog):
    """Help and information commands."""
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the Help cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        logger.info("Help cog initialized")
    
    @commands.slash_command(description="Get help on all commands")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        """
        Display help information about available commands.
        
        Args:
            inter: The interaction context
        """
        embed = disnake.Embed(
            title="🎮 Minecraft Server Bot - Commands",
            description="Manage your Minecraft server directly from Discord!",
            color=disnake.Color.green()
        )
        
        # Server Control
        embed.add_field(
            name="🔌 Server Control",
            value=(
                "`/start` - Start the Minecraft server\n"
                "`/stop` - Stop the server (only if no players online)\n"
                "`/info` - Get server status and information"
            ),
            inline=False
        )
        
        # Chat Commands
        embed.add_field(
            name="💬 Chat Commands",
            value=(
                "`/say <message>` - Send a message to Minecraft chat\n"
                "*Messages in designated channels are automatically relayed*"
            ),
            inline=False
        )
        
        # Network Commands
        embed.add_field(
            name="🌐 Network Commands",
            value=(
                "`/ipcheck` - Check server connectivity and get address info"
            ),
            inline=False
        )
        
        # Admin Commands
        embed.add_field(
            name="🔧 Admin Commands (OP Only)",
            value=(
                "`/cmd <command>` - Execute a Minecraft server command"
            ),
            inline=False
        )
        
        # Footer
        embed.set_footer(
            text="💡 Tip: The server must be running for most commands to work"
        )
        
        await inter.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Help command invoked by {inter.author}")


def setup(bot: commands.Bot):
    """
    Setup function to add this cog to the bot.
    
    Args:
        bot: The Discord bot instance
    """
    bot.add_cog(Help(bot))