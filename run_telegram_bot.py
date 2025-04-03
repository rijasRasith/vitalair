#!/usr/bin/env python
"""
Run script for the VitalAir Telegram Bot
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def run_bot():
    """Run the Telegram bot with the token from environment variables"""
    # Check if TELEGRAM_BOT_TOKEN is set
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not found.")
        logger.info("Please create a .env file with your TELEGRAM_BOT_TOKEN or set the environment variable.")
        sys.exit(1)
    
    # Import the bot code
    try:
        from telegram_bot import main
        
        # Patch the token
        import telegram_bot
        telegram_bot.TELEGRAM_TOKEN = token
        
        # Run the bot
        logger.info("Starting VitalAir Telegram Bot...")
        main()
    except ImportError as e:
        logger.error(f"Error importing telegram_bot module: {e}")
        logger.info("Make sure 'python-telegram-bot' is installed. Run: pip install python-telegram-bot>=20.0")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
        sys.exit(1)

def run_test_query():
    """Run a test query without starting the actual bot"""
    from telegram_bot import test_query
    
    # Default test query
    query = "Alandur 31-12-2024"
    
    # Check if a query was provided as an argument
    if len(sys.argv) > 2:
        query = sys.argv[2]
    
    logger.info(f"Running test query: '{query}'")
    test_query(query)

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test_query()
    else:
        run_bot() 