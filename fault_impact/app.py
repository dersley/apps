import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from util.Class_Trajectory import Trajectory


# Initialise Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# App layout
app.layout = html.Div([
    html.H1(children="Fault Impact Visualisation"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fault-impact-graph')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="Fault Offset (m)"),
            dcc.Slider(
                id="fault-offset-slider",
                min=0,
                max=20,
                step=0.1,
                value=10,
                tooltip={"always_visible": True, "placement": "top"},
                marks={i: str(i) for i in range(0, 21, 5)}
            ),
            html.H3(children="Seam Thickness (m)"),
            dcc.Slider(
                id="seam-thickness-slider",
                min=0.1,
                max=25,
                step=0.1,
                value=5,
                tooltip={"always_visible": True, "placement": "top"},
                marks={i: str(i) for i in range(0, 26, 5)}
            ),
        ], width=6),
        dbc.Col([
            html.H3(children="Maximum Approach Angle (deg)"),
            dcc.Slider(
                id="approach-angle-slider",
                min=0.1,
                max=15,
                step=0.1,
                value=3,
                tooltip={"always_visible": True, "placement": "top"},
                marks={i: str(i) for i in range(0, 16, 5)}
            ),
            html.H3(children="Dog Leg Severity (deg per 30m)"),
            dcc.Slider(
                id="dog-leg-severity-slider",
                min=0.1,
                max=8,
                step=0.1,
                value=3,
                tooltip={"always_visible": True, "placement": "top"},
                marks={i: str(i) for i in range(0, 9, 2)}
            ),
        ], width=6),
    ]),
])

# Create instance of Trajectory to modify
trajectory = Trajectory(approach_angle=3, dog_leg_severity=3, fault_offset=10, seam_thickness=5)

# Main app callback function 
@app.callback(
    Output(component_id='fault-impact-graph', component_property='figure'),
    [Input(component_id='fault-offset-slider', component_property='value'),
     Input(component_id='seam-thickness-slider', component_property='value'),
     Input(component_id='approach-angle-slider', component_property='value'),
     Input(component_id='dog-leg-severity-slider', component_property='value'),]
)
def update_graph(fault_offset, seam_thickness, approach_angle, dog_leg_severity):

    # Update class attributes
    trajectory.set_fault_offset(fault_offset)
    trajectory.set_seam_thickness(seam_thickness)
    trajectory.set_approach_angle(approach_angle)
    trajectory.set_dog_leg_severity(dog_leg_severity) 

    fig = trajectory.fault_impact_plot()

    return fig
 
# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)