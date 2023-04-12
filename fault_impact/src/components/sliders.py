from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    slider_col1 = dbc.Col([
        html.H3("Maximum Approach Angle (deg)"),
        dcc.Slider(
            id=ids.APPROACH_ANGLE_SLIDER,
            min=0,
            max=10,
            step=0.1,
            value=3,
            tooltip={"always_visible": True, "placement": "top"},
            marks={i: str(i) for i in range(0, 11, 2)}
        ),
    ], md=6)

    slider_col2 = dbc.Col([
        html.H3("Dog Leg Severity (angle build per 30m)"),
        dcc.Slider(
            id=ids.DOG_LEG_SEVERITY_SLIDER,
            min=0,
            max=10,
            step=0.1,
            value=3,
            tooltip={"always_visible": True, "placement": "top"},
            marks={i: str(i) for i in range(0, 11, 2)}
        ),
    ], md=6)

    slider_col3 = dbc.Col([
        html.H3("Fault Offset (m)"),
        dcc.Slider(
            id=ids.FAULT_OFFSET_SLIDER,
            min=0,
            max=25,
            step=0.1,
            value=10,
            tooltip={"always_visible": True, "placement": "top"},
            marks={i: str(i) for i in range(0, 26, 5)}
        ),
    ], md=6)

    slider_col4 = dbc.Col([
        html.H3("Seam Thickness (m)"),
        dcc.Slider(
            id=ids.SEAM_THICKNESS_SLIDER,
            min=0.1,
            max=25,
            step=0.1,
            value=3,
            tooltip={"always_visible": True, "placement": "top"},
            marks={i: str(i) for i in range(0, 26, 5)}
        ),
    ], md=6)

    slider_row1 = dbc.Row([slider_col1, slider_col2])
    slider_row2 = dbc.Row([slider_col3, slider_col4])
    slider_grid = dbc.Container([slider_row1, slider_row2])

    return dbc.Container([
        slider_grid,
    ])
