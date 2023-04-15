from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from . import ids
from ..utils.beta_distribution import plot_scaled_beta


def render(app: Dash) -> html.Div:

    @app.callback(
            Output(ids.DENSITY_CHART, "figure"),
            [
            Input(ids.MINMAX_FAULT_DENSITY_SLIDER, "value"),
            Input(ids.MEAN_FAULT_DENSITY_SLIDER, "value"),
            Input(ids.STDEV_FAULT_DENSITY_SLIDER, "value"),
            ]
    )
    def update_plot(
                fault_density_range: list[float],
                fault_density_mean: float,
                fault_density_stdev: float
    ):
        
        # generate beta distribution plot
        fig = plot_scaled_beta(
            min_val=fault_density_range[0],
            max_val=fault_density_range[1],
            mean=fault_density_mean,
            std_dev=fault_density_stdev
        )

        return fig

    # Create an empty graph with an ID
    graph = dcc.Graph(id=ids.DENSITY_CHART, figure={})

    # Return the graph
    return html.Div([graph])

