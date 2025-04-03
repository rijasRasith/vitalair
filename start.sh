#!/bin/bash

# Print version info
echo "Starting VitalAir application"
python --version
pip list | grep wave

# Set the Railway environment flag
export RAILWAY_ENVIRONMENT="production"

# Set the H2O_WAVE_PORT environment variable
export PORT=${PORT:-8080}
export H2O_WAVE_PORT=${PORT}
export H2O_WAVE_LISTEN="0.0.0.0:${PORT}"
export H2O_WAVE_ADDRESS="http://0.0.0.0:${PORT}"
export H2O_WAVE_APP_ADDRESS="http://127.0.0.1:8000"
export H2O_WAVE_EXTERNAL_ADDRESS="http://0.0.0.0:${PORT}"
export H2O_WAVE_NO_LOG=false

echo "Using port: $PORT"
echo "Wave port: $H2O_WAVE_PORT"
echo "Listening on: $H2O_WAVE_LISTEN"
echo "App address: $H2O_WAVE_APP_ADDRESS"
echo "External address: $H2O_WAVE_EXTERNAL_ADDRESS"

# Show current directory and files
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Use direct python runner instead of wave CLI
echo "Starting Python Wave runner..."
python run_railway.py 