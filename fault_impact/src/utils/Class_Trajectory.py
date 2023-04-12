from . import TOOL_POSITION, DISTANCE_INC, PERISCOPE_RANGE
from .fault_vis_functions_plotly import fault_impact_vis


class Trajectory:
    def __init__(self):
        # Initialize with default values
        self.approach_angle = 4
        self.dog_leg_severity = 3
        self.fault_offset = 10
        self.seam_thickness = 5

        # Project parameters from json.config
        self.tool_position = TOOL_POSITION
        self.distance_inc = DISTANCE_INC
        self.periscope_range = PERISCOPE_RANGE

    def set_approach_angle(self, approach_angle):
        self.approach_angle = approach_angle

    def set_dog_leg_severity(self, dog_leg_severity):
        self.dog_leg_severity = dog_leg_severity

    def set_fault_offset(self, fault_offset):
        self.fault_offset = fault_offset

    def set_seam_thickness(self, seam_thickness):
        self.seam_thickness = seam_thickness

    def get_approach_angle(self):
        return self.approach_angle

    def get_dog_leg_severity(self):
        return self.dog_leg_severity

    def get_fault_offset(self):
        return self.fault_offset

    def get_seam_thickness(self):
        return self.seam_thickness

    def get_periscope_range(self):
        return self.periscope_range

    def get_distance_inc(self):
        return self.distance_inc
    
    def get_tool_position(self):
        return self.tool_position

    # Main visualisation function
    def fault_impact_plot(self):

        # Get required class attributes
        distance_inc = self.get_distance_inc()
        approach_angle = self.get_approach_angle()
        dog_leg_severity = self.get_dog_leg_severity()
        fault_offset = self.get_fault_offset()
        seam_thickness = self.get_seam_thickness()
        tool_position = self.get_tool_position()
        periscope_range = self.get_periscope_range()

        # Create the trajectory plot
        fig = fault_impact_vis(
            approach_angle,
            dog_leg_severity,
            fault_offset,
            seam_thickness,
            distance_inc,
            tool_position,
            periscope_range
        )

        return fig
