import numpy as np
import scipy.stats as stats
import plotly.express as px

def plot_beta_dist(successes: int, trials: int):

    # Convert parameters to alpha and beta
    alpha = successes + 1
    beta = trials - successes + 1

    # Create plot values
    x_vals = np.linspace(0, 1, 1000)

    # Beta distribution
    pdf = stats.beta.pdf(x_vals, alpha, beta)

    # Create plot with fill under curve
    data = {'x': x_vals, 'y': pdf}
    fig = px.area(data, x='x', y='y', color_discrete_sequence=["red"])

    # Update the layout
    fig.update_layout(
        xaxis_title="P(Bad Thing)",
        yaxis_title="Relative Frequency",
        title=f"Probability of Bad Thing: {successes} Occurences out of {trials} Trials",
        showlegend=False,
        template='plotly_white'
    )

    return fig


def bad_thing_plot(
        successes: int, 
        trials: int, 
        fault_density: float, 
        lateral_length: float, 
        sims: int
        ):
    """
    Simulate probability of a bad thing happening during horizontal drilling using a historical frequency of bad thing, and an estimate of fault density to simulate fault crossings per lateral.

    Plots simulation data histogram.
    """

    # Convert observations to alpha and beta parameters of Beta Distribution
    alpha = successes + 1
    beta = trials - successes + 1

    # Create container for simulation data
    bad_things = np.zeros(sims)

    # Start simulation loop
    for i in range(sims):

        # Use fault density as lambda parameter in a Poisson distribution to estimate fault encounters over lateral length
        fault_encounters: int = stats.poisson.rvs(mu=(fault_density * lateral_length))

        # P(Bad Thing) from Beta distribution
        p_bad_thing = stats.beta.rvs(alpha, beta)

        # Use fault encounters and P(Bad Thing) to randomly draw from the binomial probability of occurrences, add result to data container
        bad_things[i] = stats.binom.rvs(n=fault_encounters, p=p_bad_thing)


    # Calculate probability that at least 1 Bad Thing happened
    p_one_bad_thing = np.count_nonzero(bad_things) / bad_things.size
    print(f"Probability of at least one Bad Thing = {p_one_bad_thing}")

    # Create results histogram
    fig = px.histogram(
        bad_things, 
        title=f"Number of Bad Things that Happened.\nChance of at least one Bad Thing = {p_one_bad_thing}",
        histnorm="probability density",
        color_discrete_sequence=["red"],
        opacity=0.5,
        )

    # Update the layout
    fig.update_layout(
        xaxis_title="Count of Bad Thing",
        yaxis_title="Probability",
        showlegend=False,
        template='plotly_white',
        bargap=0.2
    )

    fig.show()



if __name__ == "__main__":
    bad_thing_plot(
        successes=1,
        trials=50,
        fault_density=1.5,
        lateral_length=4,
        sims=10000
    )