import json

from .fault_vis_functions_plotly import *

# Run json variables
with open('fault_impact/config.json') as f:
    config = json.load(f)

DISTANCE_INC = config['DISTANCE_INC']
TOOL_POSITION = config['TOOL_POSITION']
PERISCOPE_RANGE = config['PERISCOPE_RANGE']