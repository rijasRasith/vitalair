# VitalAir: AQI and HRI Forecasting System

VitalAir is an advanced forecasting system that predicts the Air Quality Index (AQI) for 12 monitoring stations in Tamil Nadu, India, for the upcoming 28 days using machine learning techniques (Nbeats and GPR). It also calculates a Health Risk Index (HRI) based on the AQI forecasts to provide health risk assessments.

Air quality monitoring is crucial for our well-being, and this project utilizes historical daily averages of various air pollutants to build accurate models that can predict the AQI and associated health risks for each station.

## Features

- AQI forecasting for 28 days using ensemble of Nbeats and GPR models
- Health Risk Index (HRI) calculation and risk categorization
- Interactive H2O Wave dashboard for data visualization
- Telegram bot integration for remote AQI and HRI queries
- Data exploration tools for historical air quality analysis

## Module Breakdown

The repository is organized as follows:

- **app.py**: Main entry point for the H2O Wave web application
- **telegram_bot.py**: Implementation of the Telegram bot for remote queries
- **run_telegram_bot.py**: Script to run the Telegram bot as a standalone service
- **components/**: UI components for the web application
  - **navbar.py**: Navigation bar component
  - **footer.py**: Footer component
  - **layout_responsive.py**: Responsive layout settings
  - **theme.py**: Theme colors and styling
- **pages/**: Different pages/views of the web application
  - **home.py**: Landing page with project overview
  - **db.py**: Dashboard for data exploration and visualization
  - **forecast.py**: Forecast page showing AQI and HRI predictions
  - **solution.py**: Technical details about the solution approach
  - **appendix.py**: Additional technical information
- **utils/**: Helper modules
  - **load_data.py**: Functions for loading and preprocessing data
- **data/**: Contains forecast data files
  - **combined_AQI_forecast.csv**: AQI forecasts for all 12 stations
  - **combined_HRI_forecast.csv**: HRI values for all 12 stations
  - **each station training files/**: Station-specific data and models
- **notebooks/**: Jupyter notebooks for data analysis and model development
  - **EDA.ipynb**: Exploratory Data Analysis
  - **Data_Preprocess.ipynb**: Data preprocessing and feature engineering
  - **model.ipynb**: Model development and evaluation
  - **HRI_calculation.ipynb**: Health Risk Index calculation methodology

## Dependencies

### Required Packages

```
# Core Data Processing and Visualization
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
tabulate==0.9.0

# Web Application
h2o-wave==0.26.3

# Telegram Bot
python-telegram-bot>=20.0
python-dateutil==2.8.2
regex==2023.6.3
python-dotenv==1.0.0

# Machine Learning
scikit-learn==1.3.0
tensorflow==2.12.0
tcn==1.15.4
pmdarima==2.0.3

# Deployment
gunicorn==21.2.0
```

## Setup Instructions

### Prerequisites

- Python 3.9+ installed
- Git installed
- Internet connection for downloading packages

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/vitalair.git
cd vitalair
```

2. **Create and activate a virtual environment**

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory with the following variables:

```
# For Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# App configuration (optional)
PORT=10101
```

If you want to use the Telegram bot functionality, you'll need to create a bot through BotFather on Telegram and add your token.

### Running Locally

1. **Start the H2O Wave server**

If you don't have H2O Wave installed globally:

```bash
pip install h2o-wave
wave run app.py
```

If you already have the H2O Wave server:

```bash
wave run app.py
```

2. **Access the application**

Open your browser and navigate to:
```
http://localhost:10101/site
```

3. **Running the Telegram bot (optional)**

In a separate terminal, with the virtual environment activated:

```bash
python run_telegram_bot.py
```

## Data Sources

The application uses air quality data from 12 monitoring stations in Tamil Nadu, India. The historical data was used to train models that generate forecasts for the AQI and HRI values.

## License

This project is licensed under the MIT License - see the LICENSE file for details.




HRI prediction and potential health risks mapping for all those 12 stations is pending
