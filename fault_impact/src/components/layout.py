from dash import Dash, html

from . import impact_chart, sliders, parameters_button



def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            impact_chart.render(app),
            sliders.render(app),
            parameters_button.render(app),
            html.H1("Fault Density Visualisation"),
            html.Hr(),
        ],
    )