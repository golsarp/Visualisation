from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field
from jbi100_app.views.radar_plot import Radar

# import dash_core_components as dcc
from dash import dcc
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
    formation,
)


from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd

if __name__ == "__main__":
    # Create data
    print("Hello world")
    df_field = px.data.medals_long()
    df = px.data.iris()
    print("Class")
    # print(df)
    # Instantiate custom views
    # scatterplot1 = Scatterplot("Scatterplot 1", "sepal_length", "sepal_width", df)
    # scatterplot2 = Scatterplot("Scatterplot 2", "petal_length", "petal_width", df)
    field = Field("field", "x", "y", df_field)
    # stores clicked players
    # selected_players = []
    selected_players = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]

    # If selection is on
    player_select = False

    radar_plot = Radar("Radar-plot", selected_players)
    # radar_fig = radar_plot.plot_radar()
    # radar_fig.show()
    df = pd.read_csv(player_poss_path)
    teams = df["team"].unique()[:5]
    # print(teams)

    # Define the layout
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="left-column",
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
                                    html.Label("Formation"),
                                    dcc.Dropdown(
                                        id="home-formation",
                                        options=[
                                            {"label": form, "value": form}
                                            for form in formation
                                        ],
                                        value=formation[0],
                                        multi=False,
                                        placeholder="Formation",
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "30%"},
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
                                    html.Label("Formation"),
                                    dcc.Dropdown(
                                        id="away-formation",
                                        options=[
                                            {"label": form, "value": form}
                                            for form in formation
                                        ],
                                        value=formation[0],
                                        multi=False,
                                        placeholder="Opponent Team",
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "30%"},
                            ),
                            # html.Div(
                            #     [
                            #         # html.Label("Selection "),
                            #         # html.Button(
                            #         #     children="Select Players Off",
                            #         #     id="select-button",
                            #         #     n_clicks=0,
                            #         # ),
                            #     ]
                            # ),
                        ],
                        # style={
                        #     "display": "flex",
                        #     "justify-content": "space-between",
                        # },
                    ),
                    # Existing components
                    field,
                    # dcc.Graph(id="deneme", figure=radar_fig),
                ],
            ),
            html.Div(
                id="right-column",
                className="three columns",
                children=[
                    html.Button(
                        children="Select Players Off",
                        id="select-button",
                        n_clicks=0,
                    ),
                    radar_plot,
                    html.Button("Plot button", id="radar-button", n_clicks=0),
                    # dcc.Graph(id=radar_plot.html_id, figure=radar_fig),
                ],
            ),
        ],
    )

    @app.callback(
        Output(field.html_id, "figure"),
        [
            Input(field.html_id, "selectedData"),
            Input(field.html_id, "clickData"),
            Input("home-dropdown", "value"),
            Input("away-dropdown", "value"),
            Input("home-formation", "value"),
            Input("away-formation", "value"),
        ],
    )
    def update_field_1(select, click_data, home, away, home_form, away_from):
        if click_data is not None and player_select:
            print("select bool", player_select)
            # Extract information about the clicked point

            clicked_point_info = click_data["points"][0]
            # Print or use the information as needed
            clicked_name = clicked_point_info["customdata"][0]
            selected_players.append(clicked_name)

            print("Clicked point info:", clicked_name)
            print("selected player are ", selected_players)

        # print("select", select)
        # print("home form: ", home_form)
        # print("away_from form: ", away_from)

        # print(home, away)
        return field.positionPlayer(home, away, home_form, away_from)

    @app.callback(
        Output("select-button", "children"),
        [Input("select-button", "n_clicks")],
    )
    def update_output(n_clicks):
        global player_select
        global selected_players

        if n_clicks % 2 == 1:
            new_label = "Selection ON"
            player_select = True
            return new_label
        else:
            print("selection ended ")
            print(selected_players)
            player_select = False
            selected_players = []
            new_label = "Selection OFF"
            return new_label

    @app.callback(
        Output(radar_plot.html_id, "figure"),
        [Input("radar-button", "n_clicks")],
    )
    def update_radar(button):
        return radar_plot.plot_radar(selected_players)

    app.run_server(debug=False, dev_tools_ui=False)
