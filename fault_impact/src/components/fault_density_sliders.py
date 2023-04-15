from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from . import ids


def render(app: Dash) -> html.Div:

    # Define sliders for use in template
    fault_density_range_slider = dcc.RangeSlider(
            id=ids.MINMAX_FAULT_DENSITY_SLIDER,
            min=0,
            max=10,
            step=0.1,
            value=[2,6],
            marks={i: str(i) for i in range(0, 11, 2)},
            tooltip={"always_visible": True, "placement": "top"},
    )


    fault_density_mean_slider = dcc.Slider(
            id=ids.MEAN_FAULT_DENSITY_SLIDER,
            min=0,
            max=6,
            step=0.1,
            value=3,
            marks=None,
            tooltip={"always_visible": True, "placement": "bottom"},
    )

    fault_density_stdev_slider = dcc.Slider(
            id=ids.STDEV_FAULT_DENSITY_SLIDER,
            min=0.1,
            max=3,
            step=0.1,
            value=1,
            marks={i: str(i) for i in range(0, 4, 1)},
            tooltip={"always_visible": True, "placement": "bottom"},
    )

    # App callback to limit the mean slider values between min and max
    @app.callback(
            [Output(ids.MEAN_FAULT_DENSITY_SLIDER, "min"),
            Output(ids.MEAN_FAULT_DENSITY_SLIDER, "max")],
            Input(ids.MINMAX_FAULT_DENSITY_SLIDER, "value")
    )
    def get_range(slider_values: list[float]):
        min_value = slider_values[0]
        max_value = slider_values[1]

        return [min_value, max_value]
    
    # Put sliders in grid layout
    slider_col1 = dbc.Col([
        html.H3("Range"),
        fault_density_range_slider], md=6)

    slider_col2 = dbc.Col([
        html.H3("Mean"),
        fault_density_mean_slider], md=6)

    slider_col3 = dbc.Col([
        html.H3("Std Dev"),
        fault_density_stdev_slider], md=6)


    slider_row1 = slider_col1
    slider_row2 = dbc.Row([slider_col2, slider_col3])
    slider_grid = dbc.Container([slider_row1, slider_row2])

    return dbc.Container([
        slider_grid,
    ])

