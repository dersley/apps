from dash import Dash, html
from dash_bootstrap_components.themes import CERULEAN
import dash_bootstrap_components as dbc

from src.components.layout import create_layout


def main() -> None:
    app = Dash(__name__, external_stylesheets=[CERULEAN])
    app.title = "Horizontal Drilling Fault Impact: Tuning"
    app.layout = create_layout(app)
    app.run(debug=True)


if __name__ == "__main__":
    main()