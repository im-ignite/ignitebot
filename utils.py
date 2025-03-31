from functools import wraps
from config import ADMIN_IDS
from telegram import Update
from telegram.ext import CallbackContext

def admin_only(func):
    @wraps(func)
    async def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("⚠️ Sorry, this command is only available to bot administrators.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped 