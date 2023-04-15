from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    return html.Div(
        className="likelihood-slider-container",
        children=
        dcc.Slider(
            className=ids.LIKELIHOOD_SLIDER,
            id=ids.LIKELIHOOD_SLIDER,
            min=0,
            max=1,
            step=0.01,
            value=0.5,
            tooltip={"always_visible": True, "placement": "top"},
            marks={i: str(i) for i in range(0, 1, 11)},
        )
    )