import math
import numpy as np
import plotly.express as px

def fault_density_at_azimuth(f_min, f_max, azimuth, theta):
    """
    outputs the cartesian x and y coordinates of an ellipse with minor radius = f_min, major radius = f_max with axis rotation (clockwise from north) = azimuth
    also calculates the fault density associated with each coordinate
    """

    # reverse the azimuths so that rotation occurs clockwise
    azimuth = 360 - azimuth

    theta_rads = math.radians(theta)
    azimuth_rads = math.radians(azimuth)

    # x and y coordinates of rotated ellipse
    x = (f_max * math.cos(azimuth_rads) * math.cos(theta_rads) - f_min * math.sin(azimuth_rads) * math.sin(theta_rads))
    y = (f_max * math.sin(azimuth_rads) * math.cos(theta_rads) + f_min * math.cos(azimuth_rads) * math.sin(theta_rads))

    # vector at azimuth corresponding to fault density
    fault_density = math.sqrt(x**2 + y**2)

    return x, y, fault_density


def bearing_to_coordinate(bearing, distance):
    
    # convert bearing to radians
    bearing_rad = math.radians(bearing)

    # calculate x and y coordinates at new location
    x = distance * math.sin(bearing_rad)
    y = distance * math.cos(bearing_rad)
    
    # return new coordinates
    return x, y

def theta_to_bearing(theta, rotation):
    # Convert theta to radians and add the rotation angle
    theta_rad = math.radians(90-theta)
    rotation_rad = math.radians(rotation)
    theta_rotated = math.radians((math.degrees(theta_rad) + math.degrees(rotation_rad)) % 360)
    
    # Calculate the bearing from true north
    bearing = math.degrees(math.atan2(math.sin(theta_rotated), math.cos(theta_rotated)))

    # Make sure the bearing is between 0 and 360 degrees
    if bearing < 0:
        bearing += 360

    return bearing


def bearing_to_theta(bearing, baseline_rotation):
    # Convert bearing to radians
    bearing_rad = math.radians(bearing)

    # Calculate the baseline theta based on the baseline rotation
    baseline_theta_rad = math.radians((baseline_rotation + 90) % 360)

    # Calculate the rotated theta based on the baseline theta and the input bearing
    theta_rad = (baseline_theta_rad - bearing_rad) % (2 * math.pi)
    theta = (math.degrees(theta_rad)) % 360

    return theta


def fault_azimuth_plot(f_min, f_max, fault_azimuth, drilling_azimuth):
    """
    this will wrap fault_density_at_azimuth around 360 degrees and produce the ellipse plot
    """

    # theta to wrap around 360 degrees of azimuth. Note that theta = 0 corresponds to the azimuth of the ellipse, not to a North bearing
    theta = np.linspace(0, 359, 360)

    x = []
    y = []
    fault_density = []

    for i, angle in enumerate(theta):
        x = np.append(x, fault_density_at_azimuth(f_min, f_max, fault_azimuth, angle)[0])
        y = np.append(y, fault_density_at_azimuth(f_min, f_max, fault_azimuth, angle)[1])
        fault_density = np.append(fault_density, fault_density_at_azimuth(f_min, f_max, fault_azimuth, angle)[2])

        #print(f"At theta = {angle}, bearing = {round(theta_to_bearing(angle, fault_azimuth))}")
    
    # plotly express plot
    fig = px.line(
        x=x,
        y=y,
    )

    # Add lines along the major and minor axes of the ellipse
    fig.add_shape(
        type="line",
        x0=x[0], y0=y[0],
        x1=x[180], y1=y[180],
        line=dict(color="red", dash="dot", width=1)
    )
    fig.add_shape(
        type="line",
        x0=x[90], y0=y[90],
        x1=x[270], y1=y[270],
        line=dict(color="red", dash="dot", width=1)
    )

    # Find x, y and fault density at drilling azimuth
    print(f"fault_azimuth is {fault_azimuth}")

    # reverse rotation
    drilling_theta = 360 - drilling_azimuth

    # cancel out fault azimuth
    drilling_theta = ((90 + fault_azimuth) - drilling_azimuth) % 360
    

    new_bearing = theta_to_bearing(drilling_theta, fault_azimuth)
    angle_check = bearing_to_theta(new_bearing, fault_azimuth)
    print(f"new bearing is {new_bearing}. Angle check = {angle_check}")

    print(f"drilling theta = {drilling_theta}")
    drill_x, drill_y, drill_density = fault_density_at_azimuth(f_min, f_max, fault_azimuth, drilling_theta)

    # Add a compass arrow corresponding to the drilling azimuth
    fig.add_shape(
        type="line",
        x0=0, y0=0,
        x1=drill_x, y1=drill_y,
        line=dict(color="green")
    )

    # Format plot
    fig.update_layout(
        #title=f"F-min: {f_min}, F-max: {f_max}, Azimuth: {fault_azimuth}. Drilling Azimuth: {drilling_azimuth}", 
        xaxis_title='X', 
        yaxis_title='Y',
        template="plotly_white",
        height=500,
        width=500,
        )
    fig.update_xaxes(range=[-5, 5])
    fig.update_yaxes(range=[-5, 5])


    return fig


if __name__ == "__main__":  
    
    fig = fault_azimuth_plot(
        f_min=1,
        f_max=2,
        fault_azimuth=90,
        drilling_azimuth=5
    )
    fig.show()