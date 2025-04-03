from h2o_wave import ui
from components.theme import icons

def nav():
    header = ui.header_card(
        box='header',
        title='VITALAIR',
        subtitle='AQI and HRI Forecasting System',
        image='https://images.unsplash.com/photo-1534274867514-d5b47ef89ed7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=150&q=80',
        items=[
            ui.link(path='#home', label='Home', width="60px"),
            ui.link(path='#dashboard', label='Dashboard', width="90px"),
            ui.link(path='#forecast', label='Forecast', width="90px"),
            ui.link(path='#appendix', label='Appendix', width="75px"),
            ui.link(path='https://t.me/vitalair_bot', label='VitalAir Bot', width="100px", target='_blank'),
        ]
    )
    return header
