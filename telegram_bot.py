import os
import re
import pandas as pd
from datetime import datetime
import logging
import asyncio
import threading
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Path to the forecast data files
AQI_FORECAST_PATH = './data/combined_AQI_forecast.csv'
HRI_FORECAST_PATH = './data/combined_HRI_forecast.csv'

# Import the get_risk_category and get_aqi_message functions from forecast.py
from pages.forecast import get_risk_category, get_aqi_message

# Bot state tracking
is_running = False
application = None
bot_thread = None

# Load environment variables
load_dotenv()

# Get token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8033530606:AAGoKcAtDU_08oucMjU4NBaO6C80YWoSoCI")

def load_forecast_data():
    """Load both AQI and HRI forecast datasets"""
    try:
        aqi_df = pd.read_csv(AQI_FORECAST_PATH)
        hri_df = pd.read_csv(HRI_FORECAST_PATH)
        
        # Convert Date column to datetime
        aqi_df['Date'] = pd.to_datetime(aqi_df['Date'])
        hri_df['Date'] = pd.to_datetime(hri_df['Date'])
        
        return aqi_df, hri_df
    except Exception as e:
        logger.error(f"Error loading forecast data: {e}")
        return None, None

def parse_message(message_text):
    """
    Parse a message in the format "<Location> <DD-MM-YYYY>"
    Returns (location, date) tuple or (None, None) if invalid format
    """
    # Match the pattern: word followed by space and date in DD-MM-YYYY format
    pattern = r"^(\w+)\s+(\d{2}-\d{2}-\d{4})$"
    match = re.match(pattern, message_text.strip())
    
    if not match:
        return None, None
    
    location = match.group(1)
    date_str = match.group(2)
    
    # Try to parse the date
    try:
        # Parse DD-MM-YYYY format
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        # Convert to YYYY-MM-DD for dataset matching
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return location, formatted_date
    except ValueError:
        logger.error(f"Invalid date format: {date_str}")
        return location, None

def get_forecast_data(location, date_str, aqi_df, hri_df):
    """
    Get AQI and HRI forecast data for a specific location and date
    Returns a tuple of (aqi_value, aqi_category, hri_value, risk_category)
    """
    if aqi_df is None or hri_df is None:
        return None, None, None, None
    
    # Filter for the requested location and date
    aqi_data = aqi_df[(aqi_df['Location'] == location) & (aqi_df['Date'] == date_str)]
    hri_data = hri_df[(hri_df['Location'] == location) & (hri_df['Date'] == date_str)]
    
    if aqi_data.empty or hri_data.empty:
        return None, None, None, None
    
    # Extract values
    aqi_value = round(aqi_data['AQI_Forecast'].values[0], 2)
    hri_value = round(hri_data['HRI'].values[0], 4)
    
    # Determine AQI category
    aqi_category = "Good"
    if aqi_value > 300:
        aqi_category = "Hazardous"
    elif aqi_value > 200:
        aqi_category = "Very Unhealthy"
    elif aqi_value > 150:
        aqi_category = "Unhealthy"
    elif aqi_value > 100:
        aqi_category = "Unhealthy for Sensitive Groups"
    elif aqi_value > 50:
        aqi_category = "Moderate"
    
    # Determine HRI risk category
    risk_category = get_risk_category(hri_value)
    
    return aqi_value, aqi_category, hri_value, risk_category

def format_response(location, date_str, aqi_value, aqi_category, hri_value, risk_category):
    """Format the response message with AQI and HRI details"""
    if aqi_value is None or hri_value is None:
        return f"Sorry, no forecast data available for {location} on {date_str}."
    
    # Format the date for display (convert YYYY-MM-DD to DD-MM-YYYY)
    try:
        display_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    except:
        display_date = date_str
    
    # Get the AQI message
    aqi_message = get_aqi_message(aqi_category)
    
    # Format the response - Escape any special characters to avoid Markdown parsing issues
    location_escaped = location.replace("_", "\\_")
    
    # Format the response without using Markdown formatting
    response = "📊 Air Quality & Health Risk Forecast 📊\n\n"
    response += f"📍 Location: {location_escaped}\n"
    response += f"📅 Date: {display_date}\n\n"
    response += f"🌬️ Air Quality Index (AQI): {aqi_value}\n"
    response += f"🔹 Category: {aqi_category}\n"
    response += f"🔹 Status: {aqi_message}\n\n"
    response += f"⚠️ Health Risk Index (HRI): {hri_value}\n"
    response += f"🔹 Risk Level: {risk_category}\n"
    
    return response

def handle_location_date_query(message_text):
    """
    Main function to handle a location-date query message
    Returns a formatted response with forecast data
    """
    # Load forecast data
    aqi_df, hri_df = load_forecast_data()
    if aqi_df is None or hri_df is None:
        return "Sorry, forecast data is currently unavailable. Please try again later."
    
    # Parse the message
    location, date_str = parse_message(message_text)
    if location is None:
        return "Please use the format: <Location> <DD-MM-YYYY>\nFor example: 'Alandur 31-12-2024'"
    
    if date_str is None:
        return "Invalid date format. Please use DD-MM-YYYY format, e.g., '31-12-2024'"
    
    # Check if location exists in our data
    if location not in set(aqi_df['Location'].unique()) | set(hri_df['Location'].unique()):
        available_locations = sorted(set(aqi_df['Location'].unique()) | set(hri_df['Location'].unique()))
        return f"Location '{location}' not found. Available locations: {', '.join(available_locations)}"
    
    # Get the forecast data
    aqi_value, aqi_category, hri_value, risk_category = get_forecast_data(
        location, date_str, aqi_df, hri_df
    )
    
    # Format and return the response
    return format_response(location, date_str, aqi_value, aqi_category, hri_value, risk_category)

# The Telegram bot implementation using python-telegram-bot library
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to VitalAir Forecast Bot! 👋\n\n"
        "I can provide you with Air Quality Index (AQI) and Health Risk Index (HRI) forecasts for various locations in Tamil Nadu.\n\n"
        "To get a forecast, send a message in this format:\n"
        "<Location> <DD-MM-YYYY>\n\n"
        "For example: 'Alandur 31-12-2024'"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "VitalAir Bot Help 🆘\n\n"
        "To get an air quality and health risk forecast, send a message in this format:\n"
        "<Location> <DD-MM-YYYY>\n\n"
        "For example: 'Alandur 31-12-2024'\n\n"
        "Available locations include: Alandur, Vellore, Velachery, Tirupur, Salem, Royapuram, "
        "Ramanathapuram, Perungudi, Manali, Ooty, Kodungaiyur, and Crescent_chengalpattu."
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    response = handle_location_date_query(message_text)
    await update.message.reply_text(response)

def stop_bot():
    """Stop the bot gracefully"""
    global is_running, application
    if is_running and application:
        logger.info("Stopping Telegram bot...")
        application.stop()
        is_running = False

def run_bot_polling():
    """Run the bot in a background thread with polling"""
    global is_running, application
    
    # Set up new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Create the Application
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        # Run the bot
        logger.info("Starting Telegram bot...")
        is_running = True
        
        # Start the bot with the dedicated event loop
        loop.run_until_complete(application.run_polling(allowed_updates=Update.ALL_TYPES))
    except Exception as e:
        logger.error(f"Error running bot polling: {e}")
    finally:
        is_running = False
        loop.close()
        logger.info("Bot has stopped")

def main():
    """Start the bot with proper threading support"""
    global is_running, bot_thread
    
    # If already running, don't start again
    if is_running:
        logger.info("Bot is already running")
        return
    
    try:
        # Create and start a new thread for the bot
        bot_thread = threading.Thread(target=run_bot_polling, daemon=True)
        bot_thread.start()
    except Exception as e:
        logger.error(f"Error starting bot thread: {e}")
        is_running = False

# Simple test function for direct console testing
def test_query(query):
    """Test the query handling function directly"""
    response = handle_location_date_query(query)
    print(response)

# Example usage for testing
if __name__ == "__main__":
    # Test with a valid query
    test_query("Alandur 31-12-2024")
    
    # Test with an invalid location
    test_query("NonExistentLocation 31-12-2024")
    
    # Test with an invalid date format
    test_query("Alandur 2024-12-31") 