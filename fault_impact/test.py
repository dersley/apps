import matplotlib.pyplot as plt
import plotly.tools as tls

from util.Class_Trajectory import Trajectory

# Create class instance
test = Trajectory(approach_angle=4, dog_leg_severity=3.5, fault_offset=10, seam_thickness=5)

# Test plot
fig = test.fault_impact_plot()

fig.show()