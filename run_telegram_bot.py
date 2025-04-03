#!/usr/bin/env python
# Standalone script to run Telegram bot

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging - more verbose for troubleshooting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Print startup banner
print("=" * 50)
print("VITALAIR TELEGRAM BOT SERVICE")
print("=" * 50)
print(f"Python version: {sys.version}")
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())
print("=" * 50)

# Load env variables
load_dotenv()

# Get telegram token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    print("Available environment variables:", [key for key in os.environ.keys()])
    sys.exit(1)
else:
    # Print token prefix for verification (safely)
    token_prefix = TELEGRAM_TOKEN.split(":")[0] if ":" in TELEGRAM_TOKEN else TELEGRAM_TOKEN[:8]
    logger.info(f"Telegram token found. Prefix: {token_prefix}...")

async def main():
    try:
        # Import the bot asynchronously
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
        
        # Import handlers - use local imports to avoid circular imports
        logger.info("Importing handlers...")
        
        # Define handlers directly here for simplicity
        async def start(update: Update, context):
            logger.info(f"Start command received from user {update.effective_user.id}")
            await update.message.reply_text(
                "Welcome to VitalAir Forecast Bot! 👋\n\n"
                "I can provide you with Air Quality Index (AQI) and Health Risk Index (HRI) forecasts for various locations in Tamil Nadu.\n\n"
                "To get a forecast, send a message in this format:\n"
                "<Location> <DD-MM-YYYY>\n\n"
                "For example: 'Alandur 31-12-2024'"
            )

        async def help_command(update: Update, context):
            logger.info(f"Help command received from user {update.effective_user.id}")
            await update.message.reply_text(
                "VitalAir Bot Help 🆘\n\n"
                "To get an air quality and health risk forecast, send a message in this format:\n"
                "<Location> <DD-MM-YYYY>\n\n"
                "For example: 'Alandur 31-12-2024'\n\n"
                "Available locations include: Alandur, Vellore, Velachery, Tirupur, Salem, Royapuram, "
                "Ramanathapuram, Perungudi, Manali, Ooty, Kodungaiyur, and Crescent_chengalpattu."
            )

        async def message_handler(update: Update, context):
            logger.info(f"Message received from user {update.effective_user.id}: {update.message.text}")
            
            # Import the query handler
            from telegram_bot import handle_location_date_query
            
            # Process the message
            message_text = update.message.text
            response = handle_location_date_query(message_text)
            
            logger.info(f"Sending response: {response[:100]}...")
            await update.message.reply_text(response)
        
        logger.info("Starting VitalAir Telegram Bot...")
        
        # Create the application
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        # Start the bot
        logger.info("Starting polling...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=["message"])
        
        logger.info("Bot is running! Press Ctrl+C to stop")
        
        # Keep the bot running until interrupted
        try:
            # Run forever
            while True:
                await asyncio.sleep(3600)  # Sleep for an hour
                logger.info("Bot is still running...")
        except asyncio.CancelledError:
            logger.info("Bot polling was cancelled")
        finally:
            # Stop the bot gracefully
            logger.info("Stopping the bot...")
            await application.stop()
            await application.shutdown()
    
    except Exception as e:
        logger.exception(f"Error in bot main function: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run the bot using asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 