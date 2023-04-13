from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from . import ids
from ..utils.bayesian_update_functions import bayesian_update_plot


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.BAYESIAN_UPDATE_CHART, "figure"),
        Input(ids.LIKELIHOOD_SLIDER, "value")
    )
    def update_plot(likelihood: float):
        fig = bayesian_update_plot(likelihood)

        return fig

    # Create graph element for layout
    graph = dcc.Graph(id=ids.BAYESIAN_UPDATE_CHART, figure={})

    return html.Div([graph])

        


