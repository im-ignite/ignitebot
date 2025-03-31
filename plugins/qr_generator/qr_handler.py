import qrcode
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from plugins.base import BotPlugin
from logger import logger
from database import Database

class QRGeneratorPlugin(BotPlugin):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.commands = [
            ("qr", self.generate_qr, "Generate QR code from text")
        ]

    async def generate_qr(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = update.effective_user
            if not context.args:
                await update.message.reply_text(
                    "Please provide text after the command. Example: /qr Hello World"
                )
                return

            text = ' '.join(context.args)
            
            # Log the QR code generation
            self.db.add_or_update_user(user.id, user.username, user.first_name)
            self.db.log_command(user.id, "qr", text)
            self.db.log_qr_generation(user.id, text)

            logger.info(f"Generating QR code for text: {text[:30]}...")

            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save temporarily and send
            img_path = "temp_qr.png"
            img.save(img_path)
            
            with open(img_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=f"QR Code for: {text[:100]}..."
                )

            # Cleanup
            import os
            os.remove(img_path)
            
            logger.info("QR code generated and sent successfully")

        except Exception as e:
            logger.error(f"Error generating QR code: {str(e)}")
            await update.message.reply_text(
                "Sorry, there was an error generating the QR code."
            )

    def register_handlers(self, application):
        for command, handler, description in self.commands:
            application.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered command /{command} - {description}")

    def get_description(self):
        return "QR Code Generator Plugin - Generate QR codes from text" 