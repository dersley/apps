import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import numpy as np


def periscope_effective_range(angle, periscope_range, tool_position):
    """
    Calculates the effective range of the periscope tool given its depth of investigation, its position on the drill string and the angle of approach
    """
    # our approach angle is defined as steering up from a horizontal postion (90 degrees), so we take 90 - angle as the input
    angle = 90 - angle
    periscope_effective_range = (
        -tool_position * math.sin(math.radians(angle)) + periscope_range
    )

    return max(0, periscope_effective_range)


def steer(x, z, angle_ini, distance_inc):
    """
    Return the next x, y coordinate when steering from an initial angle
    """
    angle_ini_rad = math.radians(angle_ini)
    x += distance_inc * math.sin(angle_ini_rad)
    z += distance_inc * math.cos(angle_ini_rad)

    return x, z


def vertical_steerable_interval(angle_min, angle_max, dog_leg_severity, distance_inc):
    """
    Calculates the required vertical window to build from an initial angle to a final angle
    Used to optimize the path of the horizontal trajectory during the initial angle build (vertical to the approach angle)
    Also used to calculate the vertical window required to land in seam (from approach angle to coal dip)
    """

    DLS_inc = dog_leg_severity / 30

    # angle build loop
    steering = np.arange(0, 501, distance_inc)

    x = 0
    z = 0

    for i in steering:
        angle = angle_min + DLS_inc * i
        x, z = steer(x, z, angle, distance_inc)

        if angle >= angle_max + DLS_inc:
            return abs(z)
            break


def is_detected(z, angle, coal_z, periscope_range, tool_position):
    """
    Return True if the coal is within detection
    """

    # test if coal is within detection limits
    if z >= (coal_z - periscope_effective_range(angle, periscope_range, tool_position)):
        return True
    else:
        return False


def is_landing(
    z,
    angle_ini,
    angle_final,
    fault_offset,
    dog_leg_severity,
    hold,
    max_steerable_interval,
    distance_inc,
):
    """
    Return True if the landing window has been reached.
    The landing window returns us to a horizontal position in the middle of the coal seam based on our angle of approach and dog leg severity.
    """

    if hold == True and z >= (fault_offset - max_steerable_interval):
        return True

    elif z >= (
        fault_offset
        - vertical_steerable_interval(
            angle_ini, angle_final, dog_leg_severity, distance_inc
        )
    ):
        return True

    else:
        return False


def fault_impact_plot_init(seam_thickness, fault_offset):
    """
    Set up the visualisation plot for the fault impact function. Shows the faulted coal seam and the drill trajectory up until the fault intersection
    """

    fig = go.Figure()
    
    # Add the coal seam before fault
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=-50,
        y0=seam_thickness/2,
        x1=0,
        y1= -seam_thickness/2,
        fillcolor="grey",
        opacity=0.5,
    )
    
    # Add the coal seam after fault
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=0,
        y0=fault_offset + seam_thickness/2,
        x1=400,
        y1=fault_offset - seam_thickness/2,
        fillcolor="grey",
        opacity=0.5,
    )

    # Add the vertical fault line
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0= -10,
        y1= 2 + fault_offset + seam_thickness/2,
        line=dict(color="red"),
    )

    # Add the horizontal line
    fig.add_trace(
        go.Scatter(x=[-50, 0], y=[0, 0], mode="lines", line=dict(color="green"))
    )
    
    # Update the layout
    fig.update_layout(
        xaxis_title="Distance (m)",
        yaxis_title="Relative Vertical Position (m)",
        showlegend=False,
        template='plotly_white'
    )

    return fig


def fault_impact_vis(
    approach_angle,
    dog_leg_severity,
    fault_offset,
    seam_thickness,
    distance_inc,
    tool_position,
    periscope_range,
):
    """
    Returns the expected out of seam impact in m after crossing a fault by plotting the course of drilling from the fault encounter, to detecting the seam again, to re-landing in seam
    """

    # create plot object
    fig = fault_impact_plot_init(seam_thickness, fault_offset)

    # initial conditions
    drillpath = np.arange(0, 1001, distance_inc)
    x, z = 0, 0

    # create empty arrays for the x and z plots
    total_increments = int(1001 / distance_inc)
    x_plot, z_plot = np.zeros(total_increments), np.zeros(total_increments)

    # declare a breakpoint variable to track the final index of the loop
    breakpoint = 0

    coal_base = fault_offset - 0.5 * seam_thickness
    coal_top = fault_offset + 0.5 * seam_thickness

    # all angles adjusted so that 0 degrees = horizontal travelling right
    angle_ini = 0 + 90
    # approach will always be upward in this example, so the approach angle is less than the initial angle of 90
    approach_angle = 90 - approach_angle
    # assume coal dip stays constant
    land_angle = angle_ini

    # adjust dog leg severity from the commonly used angle per 30 m to a per m increment
    DLS_inc = dog_leg_severity / 30

    # control the phases of steering using boolean variables build, hold and land, as well as the point of detection by the Periscope tool
    build = False
    hold = False
    land = False
    detected = False

    # use reentry and reexit booleans to track events in the seam upon reentry
    reentry = False
    reexit = False

    # start drillpath loop
    angle = angle_ini

    # calculate vertical steerable assuming we reach approach angle
    maximum_steerable_interval = vertical_steerable_interval(
        approach_angle, land_angle, dog_leg_severity, distance_inc
    )

    for index, i in enumerate(drillpath):
        # before we realise we have encountered a fault and left seam
        if build == False:
            if i <= tool_position:
                x = i
                z = 0
            else:
                build = True
                fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text='Angle build', marker=dict(color="green", size=8)))

        # we have detected a seam exit, build angle toward seam until we reach our approach angle
        if build == True and hold == False and z < coal_base:
            if angle >= (approach_angle + DLS_inc):
                angle = angle_ini - DLS_inc * (i - tool_position)
                x, z = steer(x, z, angle, distance_inc)

            else:
                hold = True
                fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text='Approach angle reached', marker=dict(color="green", size=8)))

        # hold our approach angle until we detect the coal seam
        if hold == True and detected == False:
            angle = approach_angle
            x, z = steer(x, z, angle, distance_inc)

        # the seam is detected
        if (
            detected == False
            and is_detected(z, angle, coal_base, periscope_range, tool_position) == True
        ):
            detected = True
            fig.add_trace(go.Scatter(x=[x, x], y=[z, coal_base], mode='lines', line=dict(dash="dot", width=1, color="purple"))) 
            fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text='Seam detected', marker=dict(color="purple", size=8)))

        # once the seam is detected, we may immediately begin landing or keep holding angle until the right time
        if detected == True and land == False:
            # initiate landing as our vertical position has reached or exceeded the vertical steerable window that will return us to the centre of the coal seam
            if (
                is_landing(
                    z,
                    angle,
                    land_angle,
                    fault_offset,
                    dog_leg_severity,
                    hold,
                    maximum_steerable_interval,
                    distance_inc,
                )
                == True
            ):
                land = True
                fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text='Landing', marker=dict(color="green", size=8)))
                # this j counter allows us to return the angle build to initial conditions
                j = i
                # reset the angle_ini value so we can initiate landing from the correct angle
                angle_ini = angle

            # hold angle until ready to initiate landing
            else:
                x, z = steer(x, z, angle, distance_inc)

        # plot the landing
        if detected == True and land == True:
            angle = angle_ini + DLS_inc * (i - j)
            x, z = steer(x, z, angle, distance_inc)

            # we have reached our landing angle and are hopefully now back in seam
            if angle >= land_angle:
                fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', marker=dict(color="green", size=8)))
                breakpoint = index
                break

        # track reentry and reexit points if they occur, return a warning if a seam reexit occurs
        if reentry == False and z >= coal_base:
            reentry = True
            fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text='Seam reentry', marker=dict(color="red", size=8)))
            fig.add_trace(go.Scatter(x=[x, x], y=[z, 0], mode='lines', line=dict(color="red", dash="dot", width=1)))

        if reexit == False and z >= coal_top:
            reexit = True
            fig.add_trace(go.Scatter(x=[x], y=[z], mode='markers', text="Seam reexit", marker=dict(color="red", size=8)))

        # add the x, z coordinates to the plot
        x_plot[index] = x
        z_plot[index] = z

    # clip the x, z plot lists to the final index
    x_plot = x_plot[:breakpoint]
    z_plot = z_plot[:breakpoint]

    # Plot the trajectory
    fig.add_trace(go.Scatter(x=x_plot, y=z_plot, mode='lines', line=dict(color="green")))

    # Set the x-axis and y-axis limits
    fig.update_layout(xaxis_range=[-20, 400], yaxis_range=[-10, 40])
    fig.update_traces(textposition='top center')

    return fig
