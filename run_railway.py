#!/usr/bin/env python
# Direct Wave runner for Railway deployment

import os
import sys
import logging
from h2o_wave import main
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8080))
    
    # Configure Wave environment
    os.environ["H2O_WAVE_PORT"] = str(port)
    os.environ["H2O_WAVE_LISTEN"] = f"0.0.0.0:{port}"
    os.environ["H2O_WAVE_ADDRESS"] = "0.0.0.0"
    os.environ["H2O_WAVE_APP_ADDRESS"] = "0.0.0.0"
    
    logger.info(f"Starting VitalAir app on port {port}")
    
    # Import the app module directly
    spec = importlib.util.spec_from_file_location("app", "./app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    # Run the Wave app 
    main() 