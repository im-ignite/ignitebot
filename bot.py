from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import config
from command import ping, test
from qr_generator import generate_qr
from database import Database
from logger import logger
from utils import admin_only
import sqlite3
import traceback
from plugins.qr_generator.qr_handler import QRGeneratorPlugin
from plugins.admin.admin_handler import AdminPlugin

# Initialize database
db = Database()

# Error handler function
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
    
    # Notify user
    error_message = "An error occurred while processing your request."
    if update and update.effective_message:
        await update.effective_message.reply_text(error_message)

    # Log additional details if available
    if update:
        logger.error(
            f"User: {update.effective_user.id if update.effective_user else 'Unknown'}\n"
            f"Chat: {update.effective_chat.id if update.effective_chat else 'Unknown'}\n"
            f"Message: {update.effective_message.text if update.effective_message else 'Unknown'}"
        )

    try:
        # Get the error message
        error_msg = str(context.error)
        
        # Handle specific errors
        if isinstance(context.error, sqlite3.Error):
            await update.message.reply_text(
                "😕 Database error occurred. Please try again later."
            )
        elif "Message is too long" in error_msg:
            await update.message.reply_text(
                "⚠️ Response is too long. Please try a more specific request."
            )
        else:
            # Generic error message for users
            await update.message.reply_text(
                "😔 An error occurred while processing your request. Please try again later."
            )
            
        # Notify admin of the error (replace with your admin chat ID)
        if update.effective_user:
            error_text = f"❌ Error for user {update.effective_user.id}:\n"
            error_text += f"Command: {update.message.text if update.message else 'Unknown'}\n"
            error_text += f"Error: {traceback.format_exc()}"
            
            # Send to admin (you'll need to add admin notification logic)
            for admin_id in config.ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=error_text[:4000]  # Telegram message length limit
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin {admin_id}: {e}")
                    
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

# Wrap command handlers with try-except
async def safe_command(update: Update, context: CallbackContext, handler):
    try:
        await handler(update, context)
    except Exception as e:
        await error_handler(update, context)

class Bot:
    def __init__(self):
        self.plugins = []
        self.db = Database()  # Initialize database
        self.load_plugins()

    def load_plugins(self):
        # Load regular plugins
        self.plugins.append(QRGeneratorPlugin())
        # Load admin plugin
        self.plugins.append(AdminPlugin())
        logger.info(f"Loaded {len(self.plugins)} plugins")

    async def start(self, update: Update, context: CallbackContext):
        try:
            user = update.effective_user
            # Log user activity
            self.db.add_or_update_user(
                user.id,
                user.username,
                user.first_name
            )
            self.db.log_command(user.id, "start", "")
            
            logger.info(f"Command /start used by {user.first_name} (@{user.username})")
            
            # Basic help text for all users
            help_text = "Available commands:\n"
            help_text += "/start - Show this help message\n"
            
            # Add regular commands to help
            for plugin in self.plugins:
                for command, _, description in getattr(plugin, 'commands', []):
                    help_text += f"/{command} - {description}\n"
            
            # Only add admin commands if user is an admin
            if user.id in config.ADMIN_IDS:
                help_text += "\n👑 Admin commands:\n"
                for plugin in self.plugins:
                    for command, _, description in getattr(plugin, 'admin_commands', []):
                        help_text += f"/{command} - {description}\n"
            
            await update.message.reply_text(help_text)
            
        except Exception as e:
            logger.error(f"Error in start command: {str(e)}")

    def main(self):
        try:
            logger.info("[BOT] Bot is starting up...")
            app = Application.builder().token(config.BOT_TOKEN).build()

            # Register core commands
            app.add_handler(CommandHandler("start", self.start))

            # Register plugin commands
            for plugin in self.plugins:
                plugin.register_handlers(app)
                logger.info(f"Registered plugin: {plugin.get_description()}")

            logger.info("[OK] Bot is ready and listening for commands!")
            app.run_polling()
            
        except Exception as e:
            logger.error(f"[ERROR] Critical error: {str(e)}")

if __name__ == "__main__":
    bot = Bot()
    bot.main()
