from h2o_wave import ui

def meta_layout(q):
    # layout = ui.meta_card(box='', layouts=[])
    if (q.args['#'] == 'home') or (q.args['#'] == None):
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('content', zones=[
                        ui.zone('info_card', size='500px'),
                        ui.zone('stats', direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('aqi_card', size='33%'),
                            ui.zone('pollutants_card', size='33%'),
                            ui.zone('forecast_card', size='34%'),
                        ], size='150px'),
                        ui.zone('model_card', size='300px'),
                        ui.zone('how_card', size='350px'),
                    ]),
                    ui.zone('footer')
                ]),
            ui.layout(
                breakpoint='m',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('content', zones=[
                        ui.zone('top', direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('info_card', size='60%'),
                            ui.zone('stats_col', size='40%', zones=[
                                ui.zone('aqi_card'),
                                ui.zone('pollutants_card'),
                                ui.zone('forecast_card'),
                            ]),
                        ], size='500px'),
                        ui.zone('bottom', direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('model_card', size='40%'),
                            ui.zone('how_card', size='60%'),
                        ], size='500px'),
                    ]),
                    ui.zone('footer')
                ]),
        ])
    elif (q.args['#'] == 'dashboard'):
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('body'),
                    ui.zone('footer')
                ]),
            ui.layout(
                breakpoint='m',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone("ss_mardown"),
                    ui.zone('ss', direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('ss_sidebar', size='25%'),
                        ui.zone('ss_body', size='75%'),
                    ]),
                    ui.zone("aqi_mardown"),
                    ui.zone('db', direction=ui.ZoneDirection.ROW, size="400px", zones=[
                        ui.zone('sidebar', size='25%'),
                        ui.zone('body', size='75%'),
                    ]),
                    ui.zone('aqi_level_md'),
                    ui.zone("aqi_level"),
                    ui.zone('footer')
                ])
        ])
    elif (q.args['#'] == 'solution'):
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('sol_content'),
                    ui.zone('footer')
                ])
        ])
    elif (q.args['#'] == 'appendix'):
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('app_content'),
                    ui.zone('footer')
                ])
        ])
    elif q.args['#'] == 'forecast':  # Enhanced layout for Forecast page
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('forecast_md', size="100px"),
                    ui.zone('forecast_dropdown', size="100px"),
                    ui.zone('forecast_stats', direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('aqi_stats', size='50%'),
                        ui.zone('hri_stats', size='50%'),
                    ], size="120px"),
                    ui.zone('forecast_info', size="200px"),
                    ui.zone('forecast_plots', direction=ui.ZoneDirection.COLUMN, zones=[
                        ui.zone('aqi_forecast', size='300px'),
                        ui.zone('hri_forecast', size='300px'),
                    ]),
                    ui.zone('footer')
                ]),
            ui.layout(
                breakpoint='m',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('forecast_md', size="100px"),
                    ui.zone('forecast_dropdown', size="100px"),
                    ui.zone('forecast_stats', direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('aqi_stats', size='33%'),
                        ui.zone('hri_stats', size='33%'),
                        ui.zone('forecast_info', size='34%'),
                    ], size="150px"),
                    ui.zone('forecast_plots', direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('aqi_forecast', size='50%'),
                        ui.zone('hri_forecast', size='50%'),
                    ], size="400px"),
                    ui.zone('footer')
                ])
        ])
    else:
        # Default layout if no known hash is provided
        layout = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size="80px"),
                    ui.zone('content'),
                    ui.zone('footer')
                ])
        ])
    return layout