#!/usr/bin/env python
"""
Standalone Telegram bot for VitalAir app.
This file is meant to be run separately from the main app in production.
"""
import os
import logging
import asyncio
from dotenv import load_dotenv

# Import the necessary telegram components
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
    exit(1)

# Import the handler functions from the main telegram_bot module
from telegram_bot import start, help_command, message_handler

async def main():
    """Run the bot."""
    logger.info("Starting VitalAir Telegram Bot...")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start the Bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    logger.info("Bot started, running indefinitely")
    
    # Run the bot until interrupted
    try:
        # Keep the bot running indefinitely
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour and check again
            logger.info("Telegram bot still running...")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopping...")
        await application.updater.stop()
        await application.stop()
        logger.info("Bot stopped!")
    except Exception as e:
        logger.error(f"Error in bot main loop: {e}")
        await application.updater.stop()
        await application.stop()

if __name__ == '__main__':
    asyncio.run(main()) 