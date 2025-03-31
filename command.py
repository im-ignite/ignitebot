from telegram import Update
from telegram.ext import CallbackContext   
import time
from database import Database

db = Database()

async def test(update: Update, context: CallbackContext):
    # Log the command
    user = update.effective_user
    db.log_command(user.id, "test", "")
    
    await update.message.reply_text("✅ Test command is working!")      

async def ping(update: Update, context: CallbackContext):
    # Log the command
    user = update.effective_user
    db.log_command(user.id, "ping", "")
    
    start_time = time.time()
    message = await update.message.reply_text("Pinging... ⏳")
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
    await message.edit_text(f"Pong! 🏓 Latency: {latency}ms")
