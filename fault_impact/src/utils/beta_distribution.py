import numpy as np
import scipy.stats as stats
import plotly.express as px

def plot_scaled_beta(min_val, max_val, mean, std_dev):

    # Standardize mean and std_dev to correctly parameterize alpha and beta
    mean_std = (mean - min_val)/(max_val - min_val)
    std_dev_std = (std_dev - min_val)/(max_val - min_val)

    # Convert parameters to alpha and beta
    alpha = ((1 - mean_std) / std_dev_std**2 - 1 / mean_std) * mean_std**2
    beta = alpha * (1 / mean_std - 1)

    # To scale the distribution:
    # If X ~ Beta(α, β), then a + bX ~ Beta(α, β), where a and b are the location and scale parameters, respectively.
    loc = min_val
    scale = max_val - min_val

    # Create plot values
    x_vals = np.linspace(min_val, max_val, 500)

    # Beta distribution
    pdf = stats.beta.pdf(x_vals, alpha, beta, loc=loc, scale=scale)
    # Normalize distribution
    y_vals = pdf / scale

    # Create plot with fill under curve
    data = {'x': x_vals, 'y': y_vals}
    fig = px.area(data, x='x', y='y')

    # Add annotations for mean and standard deviation
    fig.add_shape(type="line", x0=mean, y0=0, x1=mean, y1=(stats.beta.pdf(mean, alpha, beta, loc=loc, scale=scale)/scale),
                  line=dict(color="red", width=2))

    # Update the layout
    fig.update_layout(
        xaxis_title="Fault Density (faults per km)",
        yaxis_title="Relative Frequency",
        showlegend=False,
        template='plotly_white'
    )

    return fig


if __name__ == "__main__":
    fig = plot_scaled_beta(0, 10, 5, 1.4)
    fig.show()

