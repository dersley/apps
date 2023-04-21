from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from . import ids
from ..utils.azimuth_functions import fault_azimuth_plot


def render(app: Dash) -> html.Div:

    @app.callback(
            Output(ids.AZIMUTH_CHART, "figure"),
            [
            Input(ids.MIN_FAULT_DENSITY_SLIDER, "value"),
            Input(ids.MAX_FAULT_DENSITY_SLIDER, "value"),
            Input(ids.FAULT_AZIMUTH_SLIDER, "value"),
            Input(ids.DRILLING_AZIMUTH_SLIDER, "value")
            ]
    )
    def update_plot(
                fault_density_min: float,
                fault_density_max: float,
                fault_azimuth: float,
                drilling_azimuth: float
    ):
        
        # generate fault azimuth plot
        fig = fault_azimuth_plot(
            fault_density_min, 
            fault_density_max, 
            fault_azimuth, 
            drilling_azimuth
            )

        return fig

    # Create an empty graph with an ID
    graph = dcc.Graph(id=ids.AZIMUTH_CHART, figure={})

    # Return the graph
    return html.Div(
        className="chart-container",
        children=[graph])

