from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field


from dash import html
import plotly.express as px
from dash.dependencies import Input, Output


if __name__ == "__main__":
    # Create data
    print("Hello world")
    df = px.data.iris()
    print("Class")
    # print(df)
    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", "sepal_length", "sepal_width", df)
    scatterplot2 = Scatterplot("Scatterplot 2", "petal_length", "petal_width", df)
    field = Field("field", "x", "y", df)
    # comment
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column", className="three columns", children=make_menu_layout()
            ),
            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                # children=[scatterplot1, scatterplot2],
                children=[field],
            ),
        ],
    )

    @app.callback(
        Output(field.html_id, "figure"),
        [
            # Input("select-color-scatter-1", "value"),
            # Input(scatterplot1.html_id, "selectedData"),
        ],
    )
    def update_scatter_1():
        print("Field")
        return field.positionPlayer()

    # Comment
    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"),
        [
            Input("select-color-scatter-1", "value"),
            Input(scatterplot1.html_id, "selectedData"),
        ],
    )
    def update_scatter_1(selected_color, selected_data):
        print("Plot 1 hello")
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"),
        [
            Input("select-color-scatter-2", "value"),
            Input(scatterplot1.html_id, "selectedData"),
        ],
    )
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)

    app.run_server(debug=False, dev_tools_ui=False)
