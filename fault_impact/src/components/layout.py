from dash import Dash, html

from . import (
    fault_impact_chart, 
    fault_impact_sliders, 
    impact_parameters_button, 
    fault_density_sliders, 
    fault_density_chart, 
    density_parameters_button,
    fault_azimuth_chart,
    fault_azimuth_sliders
)


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.H1("Fault Impact"),
            html.Hr(),
            fault_impact_chart.render(app),
            fault_impact_sliders.render(app),
            impact_parameters_button.render(app),
            html.Hr(),
            html.H1("Fault Density"),
            html.Hr(),
            fault_density_chart.render(app),
            fault_density_sliders.render(app),
            density_parameters_button.render(app),
            html.Hr(),
            html.H1("Fault Azimuth"),
            html.Hr(),
            fault_azimuth_chart.render(app),
            fault_azimuth_sliders.render(app)
        ],
    )