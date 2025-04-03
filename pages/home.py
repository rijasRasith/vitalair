from h2o_wave import ui
from components.theme import colors, icons

home_content = '''=
# VitalAir: Advanced AQI and HRI Forecasting System
'''

def create_home_page():
    # Main information card with app description
    info_card = ui.form_card(
        box='info_card',
        title='VitalAir: AQI and HRI Forecasting System',
        items=[
            ui.message_bar(
                type='info',
                text='Predicting Air Quality Index and Health Risk Index for Indian Cities',
            ),
            ui.image(path='https://images.unsplash.com/photo-1539617546058-1857ed7e4268?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80', width='100%', title='Air Quality Image'),
            ui.text_m('VitalAir is a state-of-the-art forecasting system designed to accurately predict air quality and associated health risks across 12 monitoring stations in Tamil Nadu, India. The system leverages advanced machine learning models to provide accurate forecasts for the next 28 days.'),
            ui.text_xl('Key Features'),
            ui.text('• AQI forecasting using Nbeats and GPR models'),
            ui.text('• Health Risk Index (HRI) prediction'),
            ui.text('• Interactive visualizations for all 12 monitoring stations'),
            ui.text('• Detailed dashboards for data exploration'),
            ui.buttons([
                ui.button(name='#forecast', label='View Forecasts', icon='Calendar'),
                ui.button(name='#dashboard', label='Explore Dashboard', icon='Dashboard'),
            ]),
        ],
    )
    
    # Quick stats cards using simple_card instead of stat_card
    aqi_card = ui.form_card(
        box='aqi_card',
        title='Air Quality Monitoring',
        items=[
            ui.text_xl('12'),
            ui.text('Stations in Tamil Nadu'),
            ui.separator(),
            ui.text('Tracking air quality across multiple regions'),
        ],
    )
    
    pollutants_card = ui.form_card(
        box='pollutants_card',
        title='Tracked Pollutants',
        items=[
            ui.text_xl('5'),
            ui.text('PM2.5, PM10, NO2, CO, O3'),
            ui.separator(),
            ui.text('Key air quality indicators monitored'),
        ],
    )
    
    forecast_card = ui.form_card(
        box='forecast_card',
        title='Forecast Period',
        items=[
            ui.text_xl('28'),
            ui.text('Days of Prediction'),
            ui.separator(),
            ui.text('Advanced forecasting for upcoming month'),
        ],
    )
    
    # Feature highlights
    model_card = ui.form_card(
        box='model_card',
        title='Machine Learning Models',
        items=[
            ui.text_xl('Advanced Forecasting Methods'),
            ui.separator(),
            ui.inline([
                ui.image(path='https://h2o.ai/platform/assets/logos/h2o-ai-color.svg', width='100px', title='H2O.ai Logo'),
                ui.text_l('Nbeats + GPR Ensemble'),
            ]),
            ui.text('Our solution combines the power of Neural Basis Expansion Analysis for Time Series (N-BEATS) and Gaussian Process Regression (GPR) for accurate forecasting with uncertainty quantification.'),
        ],
    )
    
    # How it works
    how_card = ui.markdown_card(
        box='how_card',
        title='How It Works',
        content='''
### Our Approach
VitalAir combines multiple advanced models:

1. **Data Processing**: Historical air quality data from 12 monitoring stations
2. **Model Training**: Ensemble of N-BEATS and GPR models
3. **Forecasting**: 28-day predictions for AQI and HRI
4. **Visualization**: Interactive dashboards for exploring results

### Business Applications
- **Healthcare**: Early warnings for vulnerable populations
- **Urban Planning**: Data-driven pollution control measures
- **Tourism**: Better visitor experiences with air quality insights
- **Agriculture**: Protection for crops from poor air quality
- **Education**: Informed decisions for school administrators
        ''',
    )
    
    # Create page sections
    home_page = {
        'info_card': info_card,
        'aqi_card': aqi_card,
        'pollutants_card': pollutants_card,
        'forecast_card': forecast_card,
        'model_card': model_card,
        'how_card': how_card,
    }
    
    return home_page

home_page = create_home_page()

'''
<hr/>
Air is what keeps humans alive. 
'''