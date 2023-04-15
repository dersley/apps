from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc

from src.components.layout import create_layout


def main() -> None:
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    app.title = "Horizontal Drilling Fault Impact"
    app.layout = create_layout(app)
    app.run(debug=False)


if __name__ == "__main__":
    main()