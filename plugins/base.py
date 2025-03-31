from abc import ABC, abstractmethod
from telegram.ext import CommandHandler
from config import ADMIN_IDS
from logger import logger
from database import Database

class BotPlugin(ABC):
    def __init__(self):
        self.commands = []
        self.admin_commands = []  # New list for admin-only commands
        self.db = Database()  # Add database to base plugin

    async def check_admin(self, update):
        """Check if user is admin"""
        user_id = update.effective_user.id
        is_admin = user_id in ADMIN_IDS
        if not is_admin:
            await update.message.reply_text("⚠️ This command is only available to bot administrators.")
            logger.warning(f"Non-admin user {user_id} tried to use admin command")
        return is_admin

    @abstractmethod
    def register_handlers(self, application):
        """Register command handlers for the plugin"""
        pass

    @abstractmethod
    def get_description(self):
        """Return plugin description"""
        pass 