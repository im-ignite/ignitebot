from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from plugins.base import BotPlugin
from logger import logger
from database import Database  # Import the Database class
from datetime import datetime

class AdminPlugin(BotPlugin):
    def __init__(self):
        super().__init__()
        self.db = Database()  # Initialize the database
        self.admin_commands = [
            ("stats", self.show_stats, "Show bot statistics"),
            ("users", self.list_users, "List all registered users"),
            ("userinfo", self.user_info, "Get detailed info about a user"),
            ("logs", self.get_logs, "Get recent log files")
        ]

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_admin(update):
            return

        try:
            # Get all stats from database
            stats = self.db.get_stats()
            
            stats_text = "📊 Bot Statistics:\n\n"
            stats_text += f"Total users: {stats['total_users']}\n"
            stats_text += f"Active today: {stats['active_today']}\n"
            stats_text += f"Commands used today: {stats['commands_today']}\n"
            stats_text += f"Total QR codes generated: {stats['total_qr_codes']}"
            
            await update.message.reply_text(stats_text)
            logger.info(f"Stats requested by admin {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in stats command: {str(e)}")
            await update.message.reply_text(f"Error fetching statistics: {str(e)}")

    async def list_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_admin(update):
            return

        try:
            users = self.db.get_all_users()
            
            if not users:
                await update.message.reply_text("No users found in database.")
                return

            users_text = "👥 Registered Users:\n\n"
            for user_id, username, first_name, last_seen in users[:20]:  # Show first 20 users
                # Handle None values
                username = username or "No username"
                first_name = first_name or "No name"
                last_seen = last_seen or "Never"
                
                users_text += f"• {first_name}\n"
                users_text += f"  Username: @{username}\n"
                users_text += f"  ID: {user_id}\n"
                users_text += f"  Last seen: {last_seen}\n"
                users_text += "───────────────\n"
            
            users_text += f"\nTotal users: {len(users)}"
            
            await update.message.reply_text(users_text)
            logger.info(f"User list requested by admin {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in users command: {str(e)}")
            await update.message.reply_text(f"Error fetching user list: {str(e)}")

    async def broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_admin(update):
            return

        try:
            if not context.args:
                await update.message.reply_text("Please provide a message to broadcast.")
                return

            message = ' '.join(context.args)
            # Add broadcast logic here
            await update.message.reply_text(f"Message broadcast sent: {message}")
            logger.info(f"Broadcast sent by admin {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in broadcast command: {str(e)}")
            await update.message.reply_text("Error sending broadcast.")

    async def get_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_admin(update):
            return

        try:
            import os
            log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
            
            if not log_files:
                await update.message.reply_text("No log files found.")
                return

            latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join('logs', x)))
            
            with open(os.path.join('logs', latest_log), 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=latest_log,
                    caption="Here's the latest log file."
                )
            logger.info(f"Logs sent to admin {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in logs command: {str(e)}")
            await update.message.reply_text("Error fetching log files.")

    async def user_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_admin(update):
            return

        try:
            if not context.args:
                await update.message.reply_text("Please provide a user ID. Usage: /userinfo <user_id>")
                return

            user_id = int(context.args[0])
            user_stats = self.db.get_user_stats(user_id)
            
            if not user_stats:
                await update.message.reply_text("User not found.")
                return

            username, first_name, commands_used, join_date, last_seen, qr_generated = user_stats
            
            info_text = f"📱 User Information:\n\n"
            info_text += f"Name: {first_name}\n"
            info_text += f"Username: @{username}\n"
            info_text += f"User ID: {user_id}\n"
            info_text += f"Commands used: {commands_used}\n"
            info_text += f"QR codes generated: {qr_generated}\n"
            info_text += f"Join date: {join_date}\n"
            info_text += f"Last seen: {last_seen}\n"

            # Get recent commands
            recent_commands = self.db.get_user_history(user_id)[:5]
            if recent_commands:
                info_text += "\nRecent commands:\n"
                for cmd, args, timestamp in recent_commands:
                    info_text += f"• {cmd} {args} - {timestamp}\n"

            await update.message.reply_text(info_text)
            logger.info(f"User info requested for {user_id} by admin {update.effective_user.id}")
        except ValueError:
            await update.message.reply_text("Invalid user ID format.")
        except Exception as e:
            logger.error(f"Error in userinfo command: {str(e)}")
            await update.message.reply_text("Error fetching user information.")

    def register_handlers(self, application):
        for command, handler, _ in self.admin_commands:
            application.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered admin command /{command}")

    def get_description(self):
        return "Admin Plugin - Administrative commands" 