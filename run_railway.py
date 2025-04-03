#!/usr/bin/env python
# Direct Wave runner for Railway deployment

import os
import sys
import logging
import subprocess
import time

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = os.environ.get("PORT", "8080")
    
    # Configure Wave environment
    os.environ["H2O_WAVE_PORT"] = port
    os.environ["H2O_WAVE_LISTEN"] = f"0.0.0.0:{port}"
    os.environ["H2O_WAVE_ADDRESS"] = "0.0.0.0"
    os.environ["H2O_WAVE_APP_ADDRESS"] = "0.0.0.0"
    os.environ["H2O_WAVE_EXTERNAL_ADDRESS"] = f"0.0.0.0:{port}"
    
    logger.info(f"Starting VitalAir app on port {port}")
    
    # Use subprocess to start the Wave app properly
    cmd = ["python", "-m", "h2o_wave", "run", "--no-reload", "app"]
    logger.info(f"Running command: {' '.join(cmd)}")
    
    try:
        # Execute the command and stream output to console
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream the output
        for line in process.stdout:
            print(line, end='')
            
        # Wait for process to complete
        process.wait()
        
        if process.returncode != 0:
            logger.error(f"Wave app exited with code {process.returncode}")
            sys.exit(process.returncode)
            
    except Exception as e:
        logger.error(f"Error running Wave app: {e}")
        sys.exit(1) 