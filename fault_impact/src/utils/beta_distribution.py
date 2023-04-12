import numpy as np
import scipy.stats as stats
import plotly.express as px

def plot_scaled_beta(min_val, max_val, mean, std_dev):
    alpha = ((1 - mean) / std_dev**2 - 1 / mean) * mean**2
    beta = alpha * (1 / mean - 1)
    x_vals = np.linspace(min_val, max_val, 1000)
    y_vals = stats.beta.pdf(x_vals, alpha, beta)

    data = {'x': x_vals, 'y': y_vals}
    fig = px.area(data, x='x', y='y', title='Beta Distribution Plot')
    fig.update_xaxes(title='X')
    fig.update_yaxes(title='PDF')

    # Add annotations for mean and standard deviation
    fig.add_shape(type="line", x0=mean, y0=0, x1=mean, y1=stats.beta.pdf(mean, alpha, beta),
                  line=dict(color="red", width=2))

    fig.add_shape(type="line", x0=(mean-std_dev), y0=stats.beta.pdf(mean-std_dev, alpha, beta),
                  x1=(mean+std_dev), y1=stats.beta.pdf(mean+std_dev, alpha, beta),
                  line=dict(color="red", width=2))


    return fig


if __name__ == "__main__":
    fig = plot_scaled_beta(0, 1, 0.2, 0.1)
    fig.show()

