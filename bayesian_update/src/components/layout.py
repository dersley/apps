from dash import Dash, html

from . import bayesian_update_chart, likelihood_slider


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            bayesian_update_chart.render(app),
            html.H3("Likelihood"),
            likelihood_slider.render(app)
        ],
    )