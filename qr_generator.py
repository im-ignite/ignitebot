from telegram import Update
from telegram.ext import CallbackContext
import qr_generator
from io import BytesIO

async def generate_qr(update: Update, context: CallbackContext):
    # Check if there's text after the command
    if not context.args:
        await update.message.reply_text("Please provide text after the command. Example: /qr Hello World")
        return

    text = ' '.join(context.args)
    
    # Log QR code generation
    user = update.effective_user
    db.log_command(user.id, "qr", text)
    db.log_qr_generation(user.id, text)
    
    # Create QR code
    qr = qr_generator.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    # Create image from QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to bytes
    bio = BytesIO()
    bio.name = 'qr.png'
    qr_image.save(bio, 'PNG')
    bio.seek(0)
    
    # Send the QR code image
    await update.message.reply_photo(bio, caption=f"QR Code for: {text}")
