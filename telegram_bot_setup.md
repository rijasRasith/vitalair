# VitalAir Telegram Bot Setup

This document provides instructions for setting up and running the VitalAir Telegram Bot, which allows users to query air quality and health risk forecasts for various locations in Tamil Nadu.

## Features

- Responds to queries in the format: `<Location> <DD-MM-YYYY>`
- Provides Air Quality Index (AQI) and Health Risk Index (HRI) forecasts
- Displays AQI category and health risk level based on the forecast data
- Handles multiple date formats robustly
- Provides helpful error messages for invalid queries

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Telegram account
- A Telegram bot token (obtained from BotFather)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root directory with your Telegram bot token:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Replace `your_bot_token_here` with the token you received from BotFather.

## Running the Bot

### Run in Production Mode

To run the bot in production mode:

```bash
python run_telegram_bot.py
```

The bot will start and listen for messages from users.

### Run in Test Mode

To test the bot functionality without actually starting the Telegram bot:

```bash
python run_telegram_bot.py test
```

This will run a test query with the default input "Alandur 31-12-2024".

You can also specify a custom test query:

```bash
python run_telegram_bot.py test "Velachery 01-01-2025"
```

## Bot Commands

The bot supports the following commands:

- `/start` - Introduces the bot and explains how to use it
- `/help` - Provides help information and lists available locations

## Query Format

Users can query the bot by sending a message in the following format:

```
<Location> <DD-MM-YYYY>
```

For example:
- `Alandur 31-12-2024`
- `Vellore 01-01-2025`

## Available Locations

The bot can provide forecasts for the following locations in Tamil Nadu:

- Alandur
- Vellore
- Velachery
- Tirupur
- Salem
- Royapuram
- Ramanathapuram
- Perungudi
- Manali
- Ooty
- Kodungaiyur
- Crescent_chengalpattu

## Implementation Details

The bot implementation is split into several files:

- `telegram_bot.py` - Core bot functionality and query handling
- `run_telegram_bot.py` - Script to run the bot with environment variables
- `pages/forecast.py` - Contains functions for determining AQI categories and risk levels

## Troubleshooting

If you encounter any issues while setting up or running the bot:

1. Ensure your Telegram bot token is correct and properly set in the `.env` file.
2. Verify that all required dependencies are installed.
3. Check that the forecast data files (`data/combined_AQI_forecast.csv` and `data/combined_HRI_forecast.csv`) exist and are properly formatted.
4. Review the logs for any error messages.

## License

This project is part of the VitalAir system and is subject to the same licensing terms as the main project. 