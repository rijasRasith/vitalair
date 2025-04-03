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

# Ensure the script is executable
chmod +x standalone_telegram_bot.py

# Show environment variables (hiding sensitive values)
echo "Environment variables:"
env | grep -v TOKEN | grep -v KEY | grep -v SECRET | grep -v PASSWORD

# Start the standalone bot
echo "Starting Telegram bot..."
python standalone_telegram_bot.py 