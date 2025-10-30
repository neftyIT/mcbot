"""Chat integration between Discord and Minecraft."""

import re
import disnake
from disnake.ext import commands
from minecraft import server_manager, rcon_client
from utils import (
    config,
    get_logger,
    ServerNotRunningError,
    RconConnectionError
)

logger = get_logger(__name__)


class Chat(commands.Cog):
    """Commands and events for Discord-Minecraft chat integration."""
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the Chat cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        logger.info("Chat cog initialized")
    
    @commands.slash_command(description="Send a message to Minecraft chat")
    async def say(
        self,
        inter: disnake.ApplicationCommandInteraction,
        message: str
    ):
        """
        Send a message to the Minecraft server chat.
        
        Args:
            inter: The interaction context
            message: The message to send
        """
        await inter.response.defer(ephemeral=True)
        logger.info(f"Say command invoked by {inter.author}: {message}")
        
        if not server_manager.is_running():
            await inter.edit_original_message(
                content="❌ The server is not running."
            )
            return
        
        try:
            # Send message via RCON
            username = inter.author.display_name
            rcon_client.broadcast_message(message, username)
            
            await inter.edit_original_message(
                content=f"✅ Message sent to Minecraft chat!"
            )
            logger.info(f"Message sent to Minecraft from {username}: {message}")
            
        except ServerNotRunningError:
            await inter.edit_original_message(
                content="❌ The server is not responding. It may be starting up or shutting down."
            )
        except RconConnectionError:
            await inter.edit_original_message(
                content="❌ Unable to communicate with the server."
            )
            logger.error("RCON connection failed during say command")
        except Exception as e:
            await inter.edit_original_message(
                content="❌ An error occurred while sending the message."
            )
            logger.error(f"Unexpected error in say command: {e}")
    
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        """
        Listen for messages in designated chat channels and relay to Minecraft.
        
        Args:
            message: The Discord message
        """
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Check if message is in a designated chat channel
        if not config.is_chat_channel(message.channel.id):
            return
        
        # Check if server is running
        if not server_manager.is_running():
            # Optionally send a warning
            warning = await message.channel.send(
                "⚠️ The server is not running. Your message was not sent."
            )
            await message.delete()
            # Delete warning after 5 seconds
            await warning.delete(delay=5.0)
            return
        
        try:
            # Send message to Minecraft
            username = message.author.display_name
            content = message.content
            
            rcon_client.broadcast_message(content, username)
            logger.info(f"Relayed message from {username}: {content}")
            
            # Delete the original message (bot will handle display via webhook)
            await message.delete()
            
        except ServerNotRunningError:
            warning = await message.channel.send(
                "⚠️ The server is not responding. Your message was not sent."
            )
            await message.delete()
            await warning.delete(delay=5.0)
        except Exception as e:
            logger.error(f"Error relaying message from Discord to Minecraft: {e}")
            await message.delete()
    
    async def handle_minecraft_chat(self, line: str):
        """
        Handle chat messages from Minecraft server output.
        
        This should be called by the server manager when it detects chat messages.
        
        Args:
            line: A line of server output
        """
        # Parse Minecraft chat format: "<username> message"
        # Example: "[12:34:56] [Server thread/INFO]: <Steve> Hello world"
        
        match = re.search(r'<([^>]+)>\s+(.+)$', line)
        if not match:
            return
        
        username = match.group(1)
        message = match.group(2)
        
        logger.info(f"Minecraft chat from {username}: {message}")
        
        # Send to Discord chat channels via webhook
        await self._send_to_discord_channels(username, message)
    
    async def _send_to_discord_channels(self, username: str, message: str):
        """
        Send a message to all configured Discord chat channels using webhooks.
        
        Args:
            username: Minecraft username
            message: Chat message
        """
        for channel_id in config.chat_channel_ids:
            try:
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    logger.warning(f"Chat channel {channel_id} not found")
                    continue
                
                # Get or create webhook for this channel
                webhooks = await channel.webhooks()
                webhook = None
                
                for wh in webhooks:
                    if wh.name == "MCBotChat":
                        webhook = wh
                        break
                
                if not webhook:
                    webhook = await channel.create_webhook(name="MCBotChat")
                    logger.info(f"Created webhook for channel {channel_id}")
                
                # Send message via webhook with Minecraft username
                await webhook.send(
                    content=message,
                    username=username,
                    avatar_url="https://minotar.net/avatar/{}/64.png".format(username)
                )
                
            except disnake.Forbidden:
                logger.error(f"Missing permissions for channel {channel_id}")
            except disnake.HTTPException as e:
                logger.error(f"HTTP error sending to channel {channel_id}: {e}")
            except Exception as e:
                logger.error(f"Error sending to Discord channel {channel_id}: {e}")


def setup(bot: commands.Bot):
    """
    Setup function to add this cog to the bot.
    
    Args:
        bot: The Discord bot instance
    """
    chat_cog = Chat(bot)
    bot.add_cog(chat_cog)
    
    # Register the chat handler with the server manager
    from minecraft import server_manager
    server_manager.set_output_callback(chat_cog.handle_minecraft_chat)