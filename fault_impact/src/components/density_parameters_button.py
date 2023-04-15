from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.DENSITY_PARAMETERS_BUTTON, "children"),
        Input(ids.DENSITY_PARAMETERS_BUTTON, "n_clicks"),
        State(ids.MINMAX_FAULT_DENSITY_SLIDER, "value"),
        State(ids.MEAN_FAULT_DENSITY_SLIDER, "value"),
        State(ids.STDEV_FAULT_DENSITY_SLIDER, "value"),
        prevent_initial_call=True,
    )
    def save_state(n_clicks, minmax_fault_density: list[float], mean_fault_density: float, stdev_fault_density: float):
        if n_clicks is None:
            pass
        else:
            fault_density_dict = {
                "min_fault_density": minmax_fault_density[0],
                "max_fault_density": minmax_fault_density[1],
                "mean_fault_density": mean_fault_density,
                "stdev_fault_density": stdev_fault_density
            }

            return "Parameters Saved!"

    return html.Div(
        className="button-container",
        id="density-button-container",
        children=[
            dbc.Button(
                "Save Fault Density Parameters",
                id=ids.DENSITY_PARAMETERS_BUTTON,
                color="primary",
            ),
        ]
    )