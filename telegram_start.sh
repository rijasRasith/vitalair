#!/bin/bash

# Print version info
echo "Starting VitalAir Telegram Bot Service"
python --version
pip list | grep telegram

# Set environment variables
export RAILWAY_ENVIRONMENT="production"

# Print debugging info
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Start the standalone bot
echo "Starting Telegram bot..."
python standalone_telegram_bot.py 