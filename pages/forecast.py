import pandas as pd
from h2o_wave import ui, data
from components.theme import colors, icons

def get_risk_category(hri_value):
    # Updated thresholds to directly align with AQI categories, based on reference_aqi at 75th percentile (32.32735)
    if hri_value < 1.55:  # Corresponds exactly to Good AQI (0-50)
        return "Low"
    elif hri_value < 3.09:  # Corresponds exactly to Moderate AQI (51-100)
        return "Moderate"
    elif hri_value < 4.64:  # Corresponds exactly to Unhealthy for Sensitive Groups AQI (101-150)
        return "High"
    else:  # Corresponds to Unhealthy or worse AQI (>150)
        return "Very High"

risk_mapping = {
    "Low": {
        "risk": "Low health risk.",
        "message": "Air quality is good. Continue with normal outdoor activities but follow general health guidelines."
    },
    "Moderate": {
        "risk": "Moderate health risk.",
        "message": "Individuals with respiratory or heart conditions should be cautious. Consider limiting prolonged outdoor activities."
    },
    "High": {
        "risk": "High health risk.",
        "message": "There is a high risk of respiratory and cardiovascular issues such as asthma and heart disease. Preventive measures include: purchasing high quality masks and air purifiers, and covering your face while going outside."
    },
    "Very High": {
        "risk": "Severe health risk.",
        "message": "Air quality is very poor! Everyone should take precautions. Avoid going outside, use high-quality masks, and consider air purifiers indoors."
    }
}

def forecast_page(q):
    # Load both forecast CSV files from the data folder
    try:
        aqi_df = pd.read_csv('./data/combined_AQI_forecast.csv')
        hri_df = pd.read_csv('./data/combined_HRI_forecast.csv')
    except Exception as e:
        return {
            'forecast_md': ui.markdown_card(
                box='forecast_md',
                title='Forecasted AQI and HRI',
                content=f'Error loading forecast data: {e}'
            )
        }

    # Process AQI data
    if 'Date' not in aqi_df.columns:
        return {
            'forecast_md': ui.markdown_card(
                box='forecast_md',
                title='Forecasted AQI and HRI',
                content='AQI CSV file does not contain a Date column.'
            )
        }
    aqi_df['Date'] = pd.to_datetime(aqi_df['Date'])
    aqi_df.sort_values(by='Date', inplace=True)

    # Process HRI data
    if 'Date' not in hri_df.columns:
        return {
            'forecast_md': ui.markdown_card(
                box='forecast_md',
                title='Forecasted AQI and HRI',
                content='HRI CSV file does not contain a Date column.'
            )
        }
    hri_df['Date'] = pd.to_datetime(hri_df['Date'])
    hri_df.sort_values(by='Date', inplace=True)

    # Ensure there is a Location column in both dataframes
    if 'Location' not in aqi_df.columns:
        aqi_df['Location'] = 'Unknown'
    if 'Location' not in hri_df.columns:
        hri_df['Location'] = 'Unknown'

    # Get unique locations from both CSVs and sort them alphabetically
    locations = sorted(set(aqi_df['Location'].unique()) | set(hri_df['Location'].unique()))

    # Safely get query args: if q.args is None, use an empty dict
    args = q.args or {}
    if 'forecast_location' in args:
        selected_location = args['forecast_location']
    else:
        selected_location = locations[0] if locations else 'Unknown'

    # Filter AQI and HRI data for the selected location
    aqi_location_data = aqi_df[aqi_df['Location'] == selected_location].copy()
    hri_location_data = hri_df[hri_df['Location'] == selected_location].copy()
    
    # Create a list of dates for the dropdown
    # Format dates to be more readable
    hri_location_data['Formatted_Date'] = hri_location_data['Date'].dt.strftime('%Y-%m-%d')
    dates = hri_location_data['Formatted_Date'].tolist()
    date_choices = [ui.choice(date, date) for date in dates]
    
    # Get selected date from query args, or use the first date if not selected
    if 'selected_date' in args:
        selected_date = args['selected_date']
    else:
        selected_date = dates[0] if dates else None

    # Get HRI value for the selected date and location
    if selected_date:
        selected_date_data = hri_location_data[hri_location_data['Formatted_Date'] == selected_date]
        if not selected_date_data.empty:
            specific_hri = selected_date_data['HRI'].values[0]
        else:
            specific_hri = 0
    else:
        specific_hri = 0
    
    # Get risk category and mapping
    risk_category = get_risk_category(specific_hri)
    risk_info = risk_mapping[risk_category]
    
    # Format dates in AQI data for matching with selected date
    aqi_location_data['Formatted_Date'] = aqi_location_data['Date'].dt.strftime('%Y-%m-%d')
    
    # Get AQI value for the selected date and location
    specific_aqi = 0
    if selected_date:
        aqi_date_data = aqi_location_data[aqi_location_data['Formatted_Date'] == selected_date]
        if not aqi_date_data.empty:
            specific_aqi = round(aqi_date_data['AQI_Forecast'].values[0], 2)
    
    # Create a stats section with key metrics
    # For example: average AQI for the forecast period
    aqi_data = aqi_df[aqi_df['Location'] == selected_location]
    hri_data = hri_df[hri_df['Location'] == selected_location]
    
    # For display in information card
    avg_aqi = round(aqi_data['AQI_Forecast'].mean(), 2) if not aqi_data.empty else 0
    avg_hri = round(hri_data['HRI'].mean(), 6) if not hri_data.empty else 0
    
    # Get latest available dates for each dataset
    latest_aqi_date = aqi_data['Date'].max().strftime('%Y-%m-%d') if not aqi_data.empty else "N/A"
    latest_hri_date = hri_data['Date'].max().strftime('%Y-%m-%d') if not hri_data.empty else "N/A"
    
    # Determine AQI category and color for the specific date
    aqi_category = "Good"
    aqi_color = colors['aqi']['good']
    if specific_aqi > 300:
        aqi_category = "Hazardous"
        aqi_color = colors['aqi']['hazardous']
    elif specific_aqi > 200:
        aqi_category = "Very Unhealthy"
        aqi_color = colors['aqi']['very_unhealthy']
    elif specific_aqi > 150:
        aqi_category = "Unhealthy"
        aqi_color = colors['aqi']['unhealthy']
    elif specific_aqi > 100:
        aqi_category = "Unhealthy for Sensitive Groups"
        aqi_color = colors['aqi']['unhealthy_sensitive']
    elif specific_aqi > 50:
        aqi_category = "Moderate"
        aqi_color = colors['aqi']['moderate']
    
    # Create layout with cards
    forecast_header = ui.markdown_card(
        box='forecast_md',
        title='Air Quality & Health Risk Forecasts',
        content=f'## Forecasting data for the next 28 days for {selected_location}'
    )
    
    # Location selection and time period selection cards
    forecast_controls = ui.form_card(
        box='forecast_dropdown',
        items=[
            ui.inline([
                ui.dropdown(
                    name='forecast_location',
                    label='Location',
                    placeholder='Select a location',
                    choices=[ui.choice(loc, loc) for loc in locations],
                    value=selected_location,
                    trigger=True,
                ),
                ui.dropdown(
                    name='forecast_duration',
                    label='Duration',
                    placeholder='Select forecast duration',
                    choices=[
                        ui.choice('7_days', '7 Days'),
                        ui.choice('14_days', '14 Days'),
                        ui.choice('28_days', '28 Days (Default)'),
                    ],
                    value='28_days',
                    trigger=True,
                ),
                ui.dropdown(
                    name='selected_date',
                    label='Date',
                    placeholder='Select a date',
                    choices=date_choices,
                    value=selected_date,
                    trigger=True,
                )
            ]),
        ],
    )
    
    # Statistics cards for AQI and HRI summary (using form_card instead of stat_card)
    aqi_stats_card = ui.form_card(
        box='aqi_stats',
        title='Air Quality Index',
        items=[
            ui.text_xl(str(specific_aqi)),
            ui.text(f'AQI Value • {aqi_category}'),
            ui.separator(),
            ui.text_l("Air Quality Status:"),
            ui.text(f"{aqi_category} - {get_aqi_message(aqi_category)}"),
            ui.separator(),
            ui.text(f'Selected date: {selected_date}'),
        ],
    )
    
    hri_stats_card = ui.form_card(
        box='hri_stats',
        title='Health Risk Index',
        items=[
            ui.text_xl(str(specific_hri)),
            ui.text(f'HRI Value • {risk_category}'),
            ui.separator(),
            ui.text_l(risk_info['risk']),
            ui.text(risk_info['message']),
            ui.separator(),
            ui.text(f'Selected date: {selected_date}'),
        ],
    )
    
    # Information card about the forecasts
    info_card = ui.markdown_card(
        box='forecast_info',
        title='Understanding the Forecasts',
        content=f"""
### Air Quality & Health Risk Forecasts
- **Air Quality Index (AQI)**: Measures overall air quality with values ranging from 0 (Good) to 500+ (Hazardous)
- **Health Risk Index (HRI)**: Indicates potential health risks based on air quality (Low to Very High)

**Average Values**: AQI: {avg_aqi} | HRI: {avg_hri}
**Latest Data Updated**: AQI: {latest_aqi_date} | HRI: {latest_hri_date}
        """,
    )

    # Filter the dataframes for the selected location
    aqi_df_filtered = aqi_df[aqi_df['Location'] == selected_location].copy()
    hri_df_filtered = hri_df[hri_df['Location'] == selected_location].copy()

    # Format the Date for the plots
    aqi_df_filtered['Date_str'] = aqi_df_filtered['Date'].dt.strftime('%Y-%m-%d')
    hri_df_filtered['Date_str'] = hri_df_filtered['Date'].dt.strftime('%Y-%m-%d')

    # Prepare AQI plot data
    aqi_fields = ['Date', 'AQI_Forecast', 'Location']
    aqi_rows = aqi_df_filtered[['Date_str', 'AQI_Forecast', 'Location']].values.tolist()
    aqi_plot_data = data(fields=aqi_fields, rows=aqi_rows)

    # Prepare HRI plot data
    hri_fields = ['Date', 'HRI', 'Location']
    hri_rows = hri_df_filtered[['Date_str', 'HRI', 'Location']].values.tolist()
    hri_plot_data = data(fields=hri_fields, rows=hri_rows)

    # Create a plot card for the selected location's forecasted AQI
    aqi_plot = ui.plot_card(
        box='aqi_forecast',
        title=f'AQI Forecast for {selected_location}',
        data=aqi_plot_data,
        plot=ui.plot([
            ui.mark(
                type='line',  # Changed from 'area' to 'line' for better compatibility
                x='=Date',
                y='=AQI_Forecast',
                color='=Location',
                x_scale='time',
            )
        ])
    )

    # Create a plot card for the selected location's forecasted HRI
    hri_plot = ui.plot_card(
        box='hri_forecast',
        title=f'HRI Forecast for {selected_location}',
        data=hri_plot_data,
        plot=ui.plot([
            ui.mark(
                type='line',  # Changed from 'area' to 'line' for better compatibility
                x='=Date',
                y='=HRI',
                color='=Location',
                x_scale='time',
            )
        ])
    )

    # Return all cards as a dictionary
    return {
        'forecast_md': forecast_header,
        'forecast_dropdown': forecast_controls,
        'aqi_stats': aqi_stats_card,
        'hri_stats': hri_stats_card,
        'forecast_info': info_card,
        'aqi_forecast': aqi_plot,
        'hri_forecast': hri_plot,
    }
    
def get_aqi_message(category):
    messages = {
        "Good": "Air quality is satisfactory, and air pollution poses little or no risk.",
        "Moderate": "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.",
        "Unhealthy for Sensitive Groups": "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
        "Unhealthy": "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.",
        "Very Unhealthy": "Health alert: The risk of health effects is increased for everyone.",
        "Hazardous": "Health warning of emergency conditions: everyone is more likely to be affected."
    }
    return messages.get(category, "No information available for this category.")
