from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.SAVE_PARAMETERS_BUTTON, "children"),
        Input(ids.SAVE_PARAMETERS_BUTTON, "n_clicks"),
        State(ids.APPROACH_ANGLE_SLIDER, "value"),
        State(ids.DOG_LEG_SEVERITY_SLIDER, "value"),
        State(ids.FAULT_OFFSET_SLIDER, "value"),
        State(ids.SEAM_THICKNESS_SLIDER, "value"),
        prevent_initial_call=True,
    )
    def save_state(n_clicks, approach_angle_value, dog_leg_severity_value, fault_offset_value, seam_thickness_value):
        if n_clicks is None:
            pass
        else:
            state_dict = {
                "approach_angle": approach_angle_value,
                "dog_leg_severity": dog_leg_severity_value,
                "fault_offset": fault_offset_value,
                "seam_thickness": seam_thickness_value,
            }

            return "Parameters Saved!"

    return html.Div(
        className="button-container",
        id="button-container",
        children=[
            dbc.Button(
                "Save Parameters",
                id=ids.SAVE_PARAMETERS_BUTTON,
                color="primary",
            ),
        ]
    )