#!/usr/bin/env python
"""
Standalone Telegram bot for VitalAir app.
This file is meant to be run separately from the main app in production.
"""
import os
import sys
import logging
import asyncio
import traceback
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Print environment details for debugging
logger.info(f"Python version: {sys.version}")
logger.info(f"Current directory: {os.getcwd()}")

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# Get token from environment
logger.info("Checking for Telegram bot token...")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
    logger.info("Available environment variables:")
    for key, value in os.environ.items():
        # Print keys but hide sensitive values
        logger.info(f"  {key}: {'<VALUE SET>' if value else '<NOT SET>'}")
    sys.exit(1)

logger.info("Telegram bot token found, importing dependencies...")

try:
    # Import the necessary telegram components
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    logger.info("Telegram dependencies imported successfully")
except Exception as e:
    logger.error(f"Error importing Telegram dependencies: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    # Import the handler functions from the main telegram_bot module
    logger.info("Importing handler functions from telegram_bot module...")
    from telegram_bot import start, help_command, message_handler, handle_location_date_query, load_forecast_data
    logger.info("Handler functions imported successfully")
except Exception as e:
    logger.error(f"Error importing handler functions: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test data loading
try:
    logger.info("Testing forecast data loading...")
    aqi_df, hri_df = load_forecast_data()
    if aqi_df is not None and hri_df is not None:
        logger.info(f"Forecast data loaded successfully. AQI shape: {aqi_df.shape}, HRI shape: {hri_df.shape}")
        locations = sorted(set(aqi_df['Location'].unique()) | set(hri_df['Location'].unique()))
        logger.info(f"Available locations: {', '.join(locations)}")
    else:
        logger.error("Failed to load forecast data!")
except Exception as e:
    logger.error(f"Error loading forecast data: {e}")
    traceback.print_exc()

async def main():
    """Run the bot."""
    logger.info("Starting VitalAir Telegram Bot...")
    
    try:
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
            traceback.print_exc()
            await application.updater.stop()
            await application.stop()
    except Exception as e:
        logger.error(f"Error starting Telegram bot: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error in main async loop: {e}")
        traceback.print_exc() 