import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

class BotLogFilter(logging.Filter):
    def filter(self, record):
        # Filter out HTTP API calls and telegram updates
        if any(text in record.getMessage() for text in ['HTTP Request:', 'api.telegram.org', 'getUpdates']):
            return False
        return True

class WindowsSafeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            # Replace emojis with text alternatives for Windows console
            msg = (msg.replace('🤖', '[BOT]')
                     .replace('✅', '[OK]')
                     .replace('❌', '[ERROR]')
                     .replace('⚠️', '[WARNING]'))
            self.stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

def setup_logger():
    # Set root logger level
    logging.root.setLevel(logging.WARNING)
    
    # Disable other loggers
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    # Create bot logger
    logger = logging.getLogger('TelegramBot')
    logger.setLevel(logging.INFO)
    
    # Create formatters
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    file_formatter = logging.Formatter(log_format)
    console_formatter = logging.Formatter(log_format, datefmt='%H:%M:%S')

    # Create file handler
    log_file = f'logs/bot_{datetime.now().strftime("%Y-%m-%d")}.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'  # Specify UTF-8 encoding
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(BotLogFilter())

    # Create console handler with Windows-safe output
    console_handler = WindowsSafeStreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(BotLogFilter())

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create and configure logger
logger = setup_logger()

# Example of what will be logged:
# - Bot startup and shutdown
# - Command usage
# - Errors and exceptions
# - Package installation progress
# - User interactions (without API details) 