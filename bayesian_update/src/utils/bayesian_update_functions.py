import numpy as np
import math
import plotly.graph_objects as go


def bayesian_update(prior: float, likelihood: float) -> float:
    """
    Takes a prior probability and a likelihood and returns the posterior probability
    """

    # For update posterior for valid values of likelihood
    if likelihood not in [0, 1]:
        # Convert probabilities to odds ratios
        prior_odds = prior / (1 - prior)
        likelihood_ratio = likelihood / (1 - likelihood)
        posterior_odds = prior_odds * likelihood_ratio

        posterior = posterior_odds / (posterior_odds + 1)

    # Return 0 or 1 when likelihood ratio is undefined
    elif likelihood == 1:
        posterior = 1
    elif likelihood == 0:
        posterior = 0

    return posterior


def bayesian_update_plot(likelihood):
    prior = np.arange(0, 1, 0.001)

    posterior = []
    for i in prior:
        posterior = np.append(posterior, [bayesian_update(i, likelihood)])

    fig = go.Figure()

    # change color according to direction of update
    if sum(posterior) > sum(prior):
        color = "green"
    else:
        color = "red"

    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Prior Probability"))

    if likelihood != 0 or likelihood != 1:
        fig.add_trace(
            go.Scatter(
                x=prior,
                y=posterior,
                mode="lines",
                name="Posterior Probability",
                line_color=color,
                fill="tonexty",
            )
        )

    elif likelihood == 1:
        fig.add_trace(
            go.Scatter(
                x=[0, 0, 1, 0],
                y=[0, 1, 1, 0],
                mode="lines",
                name="Posterior Probability",
                line_color=color,
                fill="toself"
            )
        )
    elif likelihood == 0:
        fig.add_trace(
            go.Scatter(
                x=[0, 1, 1, 0],
                y=[0, 0, 1, 0],
                mode="lines",
                name="Posterior Probability",
                line_color=color,
                fill="toself"
            )
        )
    

    fig.update_layout(
        xaxis_title="Prior Probability",
        yaxis_title="Posterior Probability",
        width=550,
        height=550,
        showlegend=True,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor="rgba(255, 255, 255, 0)",
            bordercolor="rgba(255, 255, 255, 0)",
        ),
        margin=dict(l=50, r=50, t=50, b=50),
    )
    fig.update_xaxes(range=[0,1])
    fig.update_yaxes(range=[0,1])

    return fig


if __name__ == "__main__":
    fig = bayesian_update_plot(1)
    fig.show()
