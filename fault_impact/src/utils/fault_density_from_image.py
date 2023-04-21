import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math


def png_to_array(png_filepath):

    # Convert image to black and white
    image = Image.open(png_filepath).convert('1')
    image_array = np.array(image)

    print(image_array[:10])

    return image_array


def create_map(png_filepath, map_scale):
    # Load the image as a NumPy array
    img_array = png_to_array(png_filepath)
    # Get the dimensions of the image array
    height, width = img_array.shape
    
    # Calculate the aspect ratio of the image
    aspect_ratio = width / height
    
    # Calculate the distance between each pixel in meters
    pixel_distance = map_scale / width
    
    # Calculate the height of the map in meters
    map_height = map_scale / aspect_ratio
    
    # Create meshgrid of x and y coordinates in meters
    x = np.arange(0, map_scale, pixel_distance)
    y = np.arange(0, map_height, pixel_distance)
    xx, yy = np.meshgrid(x, y)
    
    # Stack the meshgrid coordinates with the image array
    coords = np.dstack((xx, yy))
    map_array = np.concatenate((coords, img_array[:,:,np.newaxis]), axis=2)
    
    return map_array


def plot_random_position(map_array):
    # Extract the x, y, and pixel value arrays from the map_array
    x = map_array[:,:,0]
    y = map_array[:,:,1]

    # Get the range of x and y coordinates
    x_range = np.ptp(x)
    y_range = np.ptp(y)

    # Generate random x and y coordinates
    rand_x = np.random.rand() * x_range + np.min(x)
    rand_y = np.random.rand() * y_range + np.min(y)

    return (rand_x, rand_y)


def plot_map(map_array):
    # Extract the x, y, and pixel value arrays from the map_array
    x = map_array[:,:,0]
    y = map_array[:,:,1]
    pixel_values = map_array[:,:,2]

    # Create a scatter plot of the pixel values
    fig, ax = plt.subplots()
    ax.scatter(x.flat, y.flat, c=pixel_values.flat, cmap='gray')
    ax.set_aspect('equal')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    
    return fig, ax


def traverse_map(map_array, start_coords, distance, bearing):
    # Convert bearing to radians
    bearing_rad = math.radians(bearing)
    
    # Calculate the step size for each iteration based on the distance
    step_size = distance / map_array.shape[0]
    
    # Initialize variables
    current_coords = start_coords
    path_pixels = []
    
    # Iterate until we reach the desired distance
    while distance > 0:
        # Calculate the next coordinates based on the current bearing and step size
        next_coords = (current_coords[0] + step_size * math.cos(bearing_rad),
                       current_coords[1] + step_size * math.sin(bearing_rad))
        
        # Round the coordinates to the nearest pixel index
        x_index = int(round(next_coords[0] / map_array[1, 0, 0]))
        y_index = int(round(next_coords[1] / map_array[0, 1, 1]))
        
        # Check if the next coordinates are within the bounds of the map
        if x_index >= map_array.shape[1] or x_index < 0 or y_index >= map_array.shape[0] or y_index < 0:
            break
        
        # Add the pixel value to the path
        path_pixels.append(map_array[y_index, x_index, 2])
        
        # Update the current coordinates and remaining distance
        current_coords = next_coords
        distance -= step_size
    
    return path_pixels


if __name__ == "__main__":

    # Load in png and convert to numpy array
    fault_png = "fault_impact/static/images/fault_fabric.png"

    # Convert to map 
    fault_map = create_map(
        png_filepath=fault_png, 
        map_scale=10_000
        )
    
    print(fault_map[:10])

    # Map figure
    fig = plot_map(fault_map)

    # Generate random positions on map and plot them
    n = 10
    random_points = np.zeros((n, 2))
    
    for i in range(n):
        random_coord = plot_random_position(fault_map)

        random_points[i] = random_coord

        # Create traverses
        bearing = np.random.randint(1, 359)
        traversal = traverse_map(fault_map, random_coord, 4000, bearing)
        print(traversal)
        

    x_data = random_points[:, 0]
    y_data = random_points[:, 1]

    plt.scatter(x_data, y_data)
    plt.show()

    




