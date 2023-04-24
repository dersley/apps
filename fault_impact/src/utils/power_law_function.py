import numpy as np
import matplotlib.pyplot as plt

def plot_powerlaw(coeff, alpha, x_min, x_max, num_points=1000):

    # Create an array of x values between xmin and xmax.
    x_values = np.linspace(x_min, x_max, num_points)

    # Calculate the corresponding y values using the power-law equation.
    y_values = coeff * x_values**(-alpha)

    # Create a log-log plot of the power-law.
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    ax.set_xlabel('x')
    ax.set_ylabel('P(x)')
    ax.set_title('Power-law distribution')
    plt.show()


if __name__ == "__main__":

    plot_powerlaw(8.1, 0.731, 0, 1000)
