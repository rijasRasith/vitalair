#!/bin/bash

# Print version info
echo "Starting VitalAir application"
python --version
pip list | grep wave

# Set the H2O_WAVE_PORT environment variable
export H2O_WAVE_PORT=${PORT:-10101}
export H2O_WAVE_LISTEN="0.0.0.0:${H2O_WAVE_PORT}"
export H2O_WAVE_ADDRESS="0.0.0.0"
export H2O_WAVE_APP_ADDRESS="0.0.0.0"
export H2O_WAVE_NO_LOG=true

echo "Using port: $H2O_WAVE_PORT"
echo "Listening on: $H2O_WAVE_LISTEN"

# Use direct python runner instead of wave CLI
python run_railway.py 