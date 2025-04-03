from h2o_wave import app, main, Q
from components.navbar import nav
from components.footer import foot
from components import layout_responsive
from components.theme import get_theme
from pages import db, appendix, home, solution, forecast
import threading
import os
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Flag to track if bot is already running
bot_thread = None

def start_telegram_bot():
    """Start the Telegram bot in a separate thread"""
    # In Railway, the Telegram bot runs as a separate service
    # Only start the bot in local development environment
    if os.environ.get('RAILWAY_ENVIRONMENT') == 'production':
        logger.info("Running in Railway - Telegram bot should be running as a separate service")
        return
        
    try:
        # Check if TELEGRAM_BOT_TOKEN is set
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            logger.warning("TELEGRAM_BOT_TOKEN not found. Telegram bot will not start.")
            return

        # Import the telegram bot
        try:
            from telegram_bot import main as bot_main
            import telegram_bot
            # Set the token
            telegram_bot.TELEGRAM_TOKEN = token
            
            # Start the bot
            logger.info("Starting VitalAir Telegram Bot...")
            bot_main()
        except ImportError as e:
            logger.error(f"Could not import telegram_bot module: {e}")
            logger.info("Make sure python-telegram-bot is installed.")
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in Telegram bot thread: {e}")

@app('/site')
async def server(q: Q):
    # Start Telegram bot if not already running and not in Railway
    global bot_thread
    if os.environ.get('RAILWAY_ENVIRONMENT') != 'production' and (bot_thread is None or not bot_thread.is_alive()):
        bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
        bot_thread.start()
        logger.info("Telegram bot thread started")
    
    # Apply the custom theme to the entire app
    if not q.client.initialized:
        q.page['meta'] = await q.run(layout_responsive.meta_layout, q)
        q.page['theme'] = get_theme()
        q.client.initialized = True
    else:
        q.page['meta'] = await q.run(layout_responsive.meta_layout, q)
        
    q.page['header'] = await q.run(nav)
    q.page['footer'] = await q.run(foot)
    
    hash = q.args['#']
    
    if (hash is None) or (hash == "home"):
        # Add all home page cards
        for card_name, card in home.home_page.items():
            q.page[card_name] = card
    elif hash == "dashboard":
        # q.page['state_pie'] = await q.run(db.state_pie_chart, q)
        q.page['ss_mardown'] = db.ss_md_zone
        q.page['aqi_mardown'] = db.aqi_md_zone
        q.page['aqi_level_md'] = db.aqi_level_md_zone
        

        ## ------------------ AQI Level Distribution ------------------ ##
        q.page['aqi_level'] = await q.run(db.aqi_level_bar, q)

        ## ------------------ Cache the State-Station Pairs ------------------ ##
        if q.client.ss_state is None:
            q.client.ss_state = 'AS'
            q.client.ss_station = None
        if q.client.ss_col is None:
            q.client.ss_col = ['O3']

        if q.args.ss_state:
            if q.client.ss_state != q.args.ss_state:
                q.args.ss_station = None
            q.client.ss_state = q.args.ss_state
            q.client.ss_station = None
        
        if q.args.ss_station:
            q.client.ss_station = q.args.ss_station
        if q.args.ss_col or q.args.ss_col == []:
            q.client.ss_col = q.args.ss_col       

        ## ------------------ Distribution of Different Features in the Dataset ------------------ ##
        q.page['ss_sidebar1'] = await q.run(db.ss_state_bar_menu, q)
        q.page['ss_sidebar2'] = await q.run(db.ss_station_bar_menu, q)
        q.page['ss_sidebar3'] = await q.run(db.ss_col_bar_menu, q)

        if q.client.ss_station:
            q.page['ss_body'] = await q.run(db.plot_ss_cols, q)

        ## ------------------ AQI Dsitribution for State-Station Pairs ------------------ ##
        if q.client.state is None:
            q.client.state = 'AS'
            q.client.station = []

        if q.args.state:
            if q.client.state != q.args.state:
                q.args.station = []
            q.client.state = q.args.state
            q.client.station = []
        
        if q.args.station or q.args.station == []:
            q.client.station = q.args.station

        q.page['sidebar1'] = await q.run(db.state_bar_menu, q)
        q.page['sidebar2'] = await q.run(db.station_bar_menu, q)

        # if q.client.station or q.args.station == []:
        q.page['body'] = await q.run(db.plot_aqi, q)
    elif hash == "forecast":
        # Render the Forecast page cards with improved UI
        page_cards = forecast.forecast_page(q)
        for key, card in page_cards.items():
            q.page[key] = card
            
    elif hash == "solution":
        q.page['solution'] = solution.sol_md
    elif hash == "appendix":
        q.page['appendix'] = appendix.appendix
    await q.page.save()

# Add this section for Railway deployment
if __name__ == "__main__":
    # Get port from environment variable or use default
    port = os.environ.get("PORT", "10101")
    
    # Print startup message
    logger.info(f"Starting VitalAir application on port {port}")
    
    # Note: Environment variables should be set before importing this module
    logger.info("App will be launched by the Wave server")