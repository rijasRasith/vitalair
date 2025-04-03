from h2o_wave import ui
from components.theme import colors

def foot():
    footer = ui.footer_card(
        box='footer',
        caption='© 2023 VITALAIR - Advanced AQI and HRI Forecasting System',
        items=[
            ui.inline(justify='end', items=[
                ui.text_xl('Team'),
                ui.links(width='240px', items=[
                    ui.link(label='Rasith Novfal S', path='https://www.linkedin.com/in/rasithnovfal', target='_blank'),
                    ui.link(label='GitHub', path='https://github.com/rijasRasith', target='_blank'),
                ]),
                ui.links(width='240px', items=[
                    ui.link(label='Yogesh', path='https://www.linkedin.com/in/yogesh-sajithkumar-8a9471268/', target='_blank'),
                    ui.link(label='GitHub', path='https://github.com/Yogesh0518', target='_blank'),
                ]),
            ]),
        ],
        commands=[
            ui.command(name='feedback', label='Send Feedback'),
            ui.command(name='help', label='Help'),
        ]
    )
    return footer