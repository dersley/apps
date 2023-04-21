from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    # Define sliders for use in template
    fault_density_min_slider = dcc.Slider(
            id=ids.MIN_FAULT_DENSITY_SLIDER,
            min=0,
            max=5,
            step=0.1,
            value=2,
            marks={i: str(i) for i in range(0, 5, 1)},
            tooltip={"always_visible": True, "placement": "top"},
    )

    fault_density_max_slider = dcc.Slider(
            id=ids.MAX_FAULT_DENSITY_SLIDER,
            min=0,
            max=5,
            step=0.1,
            value=3,
            marks={i: str(i) for i in range(0, 5, 1)},
            tooltip={"always_visible": True, "placement": "top"},
    )

    fault_azimuth_slider = dcc.Slider(
            id=ids.FAULT_AZIMUTH_SLIDER,
            min=0,
            max=180,
            step=1,
            value=90,
            marks={i: str(i) for i in range(0, 179, 45)},
            tooltip={"always_visible": True, "placement": "bottom"},
    )

    drilling_azimuth_slider = dcc.Slider(
            id=ids.DRILLING_AZIMUTH_SLIDER,
            min=0,
            max=360,
            step=1,
            value=90,
            marks={i: str(i) for i in range(0, 359, 45)},
            tooltip={"always_visible": True, "placement": "bottom"},
    )

    
    # Put sliders in grid layout
    slider_1 = dbc.Col([
        html.H3("Minimum Fault Density"),
        fault_density_min_slider], md=6)

    slider_2 = dbc.Col([
        html.H3("Maximum Fault Density"),
        fault_density_max_slider], md=6)

    slider_3 = dbc.Col([
        html.H3("Fault Azimuth"),
        fault_azimuth_slider], md=6)

    slider_4 = dbc.Col([
        html.H3("Drilling Azimuth"),
        drilling_azimuth_slider], md=6)

    slider_row1 = dbc.Row([slider_1, slider_2])
    slider_row2 = dbc.Row([slider_3, slider_4])
    slider_grid = dbc.Container([slider_row1, slider_row2])

    return dbc.Container([
        slider_grid,
    ])

