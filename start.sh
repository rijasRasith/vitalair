#!/bin/bash

# Print version info
echo "Starting VitalAir application"
python --version
pip list | grep wave

# Set the H2O_WAVE_PORT environment variable
export H2O_WAVE_PORT=${PORT:-10101}
echo "Using port: $H2O_WAVE_PORT"

# Start the Wave app 
python -m h2o_wave run --no-reload app 