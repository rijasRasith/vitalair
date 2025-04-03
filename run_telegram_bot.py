#!/usr/bin/env python
# Standalone script to run Telegram bot

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load env variables
load_dotenv()

# Get telegram token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    sys.exit(1)

async def main():
    # Import the bot asynchronously
    from telegram_bot import Application, CommandHandler, MessageHandler, filters
    from telegram_bot import start, help_command, message_handler
    
    logger.info("Starting VitalAir Telegram Bot...")
    
    # Create the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start the bot
    logger.info("Starting polling...")
    await application.start_polling(allowed_updates=["message"])
    
    # Run the bot until user presses Ctrl-C
    await application.updater.stop()

if __name__ == "__main__":
    try:
        # Run the bot using asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1) 