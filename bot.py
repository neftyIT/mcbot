import sys
import disnake
from disnake.ext import commands

# Import utilities
from utils import (
    init_config,
    setup_logging,
    get_logger,
    ConfigurationError
)

# Import Minecraft modules
from minecraft import init_rcon, init_server_manager


def main():
    """Main entry point for the bot."""
    
    # Setup logging first
    setup_logging(
        log_level="INFO",
        log_file="bot.log",
        log_to_console=True
    )
    
    logger = get_logger(__name__)
    logger.info("=" * 50)
    logger.info("Starting Minecraft Discord Bot")
    logger.info("=" * 50)
    
    # Load and validate configuration
    try:
        config = init_config(".env")
        logger.info("Configuration loaded and validated successfully")
        
        # Initialize Minecraft managers AFTER config is loaded
        init_rcon()
        init_server_manager()
        logger.info("Minecraft managers initialized")
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Create bot instance
    intents = disnake.Intents.default()
    intents.message_content = True  # Required for reading messages
    
    bot = commands.Bot(
        command_prefix="!",  # Not used, but required
        intents=intents,
        sync_commands_debug=True
    )
    
    @bot.event
    async def on_ready():
        """Called when the bot is ready."""
        logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")
        logger.info(f"Connected to {len(bot.guilds)} guild(s)")

            # Log guild names
        for guild in bot.guilds:
            logger.info(f"  - {guild.name} (ID: {guild.id})")
        
        # Set bot presence
        await bot.change_presence(
            activity=disnake.Game(name="/help for commands")
        )
        
        logger.info("Bot is ready!")
    
    @bot.event
    async def on_slash_command_error(
        inter: disnake.ApplicationCommandInteraction,
        error: Exception
    ):
        """Handle slash command errors."""
        logger.error(f"Command error: {error}", exc_info=True)
        
        if inter.response.is_done():
            await inter.edit_original_message(
                content="❌ An error occurred while processing the command."
            )
        else:
            await inter.response.send_message(
                content="❌ An error occurred while processing the command.",
                ephemeral=True
            )
    
    # Load all cogs
    cogs_to_load = [
        "cogs.server_control",
        "cogs.server_info",
        "cogs.chat",
        "cogs.admin",
        "cogs.help",
    ]
    
    for cog in cogs_to_load:
        try:
            bot.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")
        except Exception as e:
            logger.error(f"Failed to load cog {cog}: {e}")
    
    # Start the bot
    try:
        logger.info("Starting bot...")
        bot.run(config.bot_token)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()