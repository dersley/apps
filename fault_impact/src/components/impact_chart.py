from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from . import ids
from ..utils.Class_Trajectory import Trajectory


def render(app: Dash) -> html.Div:

    # Initialise class instance
    trajectory = Trajectory()

    @app.callback(
            Output(ids.IMPACT_CHART, "figure"),
            [
            Input(ids.APPROACH_ANGLE_SLIDER, "value"),
            Input(ids.DOG_LEG_SEVERITY_SLIDER, "value"),
            Input(ids.FAULT_OFFSET_SLIDER, "value"),
            Input(ids.SEAM_THICKNESS_SLIDER, "value")
            ]
    )
    def update_plot(
            approach_angle: int,
            dog_leg_severity: int,
            fault_offset: int,
            seam_thickness: int,
    ):
        
        # update parameters
        trajectory.set_approach_angle(approach_angle)
        trajectory.set_dog_leg_severity(dog_leg_severity)
        trajectory.set_fault_offset(fault_offset)
        trajectory.set_seam_thickness(seam_thickness)
        
        # generate figure
        fig = trajectory.fault_impact_plot()

        return fig

    # Create an empty graph with an ID
    graph = dcc.Graph(id=ids.IMPACT_CHART, figure={})

    # Return the graph
    return html.Div([graph])

