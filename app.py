from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field
import dash_core_components as dcc
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
)


from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

if __name__ == "__main__":
    # Create data
    print("Hello world")
    df_field = px.data.medals_long()
    df = px.data.iris()
    print("Class")
    # print(df)
    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", "sepal_length", "sepal_width", df)
    # scatterplot2 = Scatterplot("Scatterplot 2", "petal_length", "petal_width", df)
    field = Field("field", "x", "y", df_field)
    # import plotly.express as px

    # df = px.data.medals_long()

    # fig = px.scatter(df, y="nation", x="count", color="medal", symbol="medal")
    # fig.update_traces(marker_size=10)
    # fig.show()
    df = pd.read_csv(player_poss_path)
    teams = df["team"].unique()[:5]
    print(teams)

    # comment
    # Define the layout
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
                children=[
                    # New input boxes at the top
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Home Team"),
                                    dcc.Dropdown(
                                        id="home-dropdown",
                                        options=[
                                            {"label": team, "value": team}
                                            for team in teams
                                        ],
                                        value="Australia",
                                        multi=False,
                                        placeholder="Home Team",
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "48%"},
                            ),
                            html.Div(
                                [
                                    html.Label("Away Team"),
                                    dcc.Dropdown(
                                        id="away-dropdown",
                                        options=[
                                            {"label": team, "value": team}
                                            for team in teams
                                        ],
                                        value="Wales",
                                        multi=False,
                                        placeholder="Opponent Team",
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "48%"},
                            ),
                        ],
                        style={"display": "flex", "justify-content": "space-between"},
                    ),
                    # Existing components
                    field,
                ],
            ),
        ],
    )

    @app.callback(
        Output(field.html_id, "figure"),
        [
            Input(field.html_id, "selectedData"),
            Input("home-dropdown", "value"),
            Input("away-dropdown", "value"),
        ],
    )
    def update_field_1(select, home, away):
        print("Field executed")
        # for selected data with box and lasso selection
        # print("select", select)
        print(home, away)
        return field.positionPlayer(home, away)

    # for sleecting points on the field
    # @app.callback(Output("output", "children"), [Input(field.html_id, "relayoutData")])
    # def display_selected_data(relayout_data):
    #     return f"Relayout Data: {relayout_data}"

    # # Comment
    # # Define interactions
    # @app.callback(
    #     Output(scatterplot1.html_id, "figure"),
    #     [
    #         Input("select-color-scatter-1", "value"),
    #         Input(scatterplot1.html_id, "selectedData"),
    #     ],
    # )
    # def update_scatter_1(selected_color, selected_data):
    #     print("Plot 1 hello")
    #     return scatterplot1.update(selected_color, selected_data)

    # @app.callback(
    #     Output(scatterplot2.html_id, "figure"),
    #     [
    #         Input("select-color-scatter-2", "value"),
    #         Input(scatterplot1.html_id, "selectedData"),
    #     ],
    # )
    # def update_scatter_2(selected_color, selected_data):
    #     return scatterplot2.update(selected_color, selected_data)

    app.run_server(debug=False, dev_tools_ui=False)
