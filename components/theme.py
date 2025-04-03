from h2o_wave import ui

def get_theme():
    return ui.theme(
        name='vitalair_theme',
        primary='#1E88E5',  # Blue - representing clean air/sky
        text='#333333',     # Dark gray for readability
        card='#FFFFFF',     # White background for cards
        page='#F5F7FA',     # Light blue-gray for page background
    )

# Define a set of consistent colors for use across the app
colors = {
    'aqi': {
        'good': '#4CAF50',
        'moderate': '#CDDC39',
        'unhealthy_sensitive': '#FFC107',
        'unhealthy': '#FF9800',
        'very_unhealthy': '#F44336',
        'hazardous': '#9C27B0'
    },
    'primary': '#1E88E5',
    'secondary': '#00ACC1',
    'accent': '#FF5722',
    'background': '#F5F7FA',
    'card': '#FFFFFF',
    'text': '#333333',
    'light_text': '#757575',
    'hri': {
        'low': '#4CAF50',
        'moderate': '#FFC107',
        'high': '#F44336'
    }
}

# Icons for different sections
icons = {
    'home': 'Home',
    'dashboard': 'Dashboard',
    'forecast': 'Calendar',
    'appendix': 'Citation',
    'air': 'CloudQueue',
    'health': 'Favorite',
    'location': 'Place',
    'settings': 'Settings'
} 