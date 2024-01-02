from jbi100_app.main import app
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field
from jbi100_app.views.radar_plot import Radar
from jbi100_app.views.team_plot import Bar
from jbi100_app.views.table import Table

import time
from jbi100_app.views.historic import Historic

# import dash_core_components as dcc
from dash import dcc, dash_table
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
    # clicked players, initially set to some players
    selected_players = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]

    all_players = ["Aaron Mooy", "Aaron Ramsey", "Brennan Johnson"]

    # selected teams
    selected_teams = ["Australia", "Wales"]

    # team features
    # TODO: add dropdown selection
    features = ["dribbles_completed_pct", "passes_pct_short", "shots_on_target_pct"]

    # If selection is on
    player_select = False

    # Field object
    field = Field("Footbal Field", "x", "y")

    # radar plot
    radar_plot = Radar("Radar-plot", selected_players)
    # historical plot
    historic_plot = Historic("Historic-plot")

    # # home bench
    # df_home = field.process_df(selected_teams[0], True)
    # # Bench players also extracted
    # df_home_field, df_home_bench = field.select_players(df_home, formation[0])
    # home_bench = df_home_bench[["player", "position", "birth_year"]]
    home_bench = None

    home_table = Table("home-table")

    away_table = Table("away-table")
    home_bench = None

    # first 5 teams initially
    # there are 32 teams, idk how to display them nicely
    df = pd.read_csv(player_poss_path)
    teams = df["team"].unique()[:5]

    # team plot
    team_plot = Bar("Team-plot", selected_players, selected_teams, features)

    # Define the layout
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="left-column",
                className="eight columns",
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
                                        style={"width": "70%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "25%"},
                            ),
                            html.Div(
                                [
                                    html.Label("Home Formation"),
                                    dcc.Dropdown(
                                        id="home-formation",
                                        options=[
                                            {"label": form, "value": form}
                                            for form in formation
                                        ],
                                        value=formation[0],
                                        multi=False,
                                        placeholder="Formation",
                                        style={"width": "70%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "25%"},
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
                                        style={"width": "70%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "25%"},
                                # style={"flex": "1", "margin": 0, "padding": 0},
                            ),
                            html.Div(
                                [
                                    html.Label("Away Formation"),
                                    dcc.Dropdown(
                                        id="away-formation",
                                        options=[
                                            {"label": form, "value": form}
                                            for form in formation
                                        ],
                                        value=formation[0],
                                        multi=False,
                                        placeholder="Opponent Team",
                                        style={"width": "70%"},
                                    ),
                                ],
                                style={"display": "inline-block", "width": "25%"},
                            ),
                        ],
                    ),
                    # Existing components
                    # field object
                    field,
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4("Home Bench"),
                                    html.P(id="table_out_home"),
                                    html.P(id="table_out_home_high"),
                                    # home_table,
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "30%",
                                    "margin-right": "80px",  # Add margin to the right
                                },
                            ),
                            html.Div(
                                [
                                    html.H4("Away Bench"),
                                    html.P(id="table_out_away"),
                                    html.P(id="table_out_away_high"),
                                    # home_table,
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "30%",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                        },
                    ),
                ],
            ),
            html.Div(
                id="right-column",
                className="four columns",
                children=[
                    # radar plot
                    radar_plot,
                    html.Button("Plot button", id="radar-button", n_clicks=0),
                    html.Button(
                        children="Select Players Off",
                        id="select-button",
                        n_clicks=0,
                    ),
                    # team plot
                    team_plot,
                    historic_plot,
                ],
            ),
        ],
    )

    @app.callback(
        Output("select-button", "children"),
        [Input("select-button", "n_clicks")],
    )
    def update_output(n_clicks):
        # global used for player selection
        global player_select
        global selected_players

        if n_clicks % 2 == 1:
            new_label = "Reset"
            player_select = True
            return new_label
        else:
            player_select = False
            selected_players = []
            new_label = "Select Players"
            return new_label

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
    def update_field(select, click_data, home, away, home_form, away_from):
        # get selected players
        if click_data is not None and player_select:
            # Extract information about the clicked point
            clicked_point_info = click_data["points"][0]
            clicked_name = clicked_point_info["customdata"][0]
            selected_players.append(clicked_name)

        player_pos, player_df, home_t, away_t = field.positionPlayer(
            home, away, home_form, away_from
        )

        global all_players
        all_players = player_df["player"].unique()
        # for tables
        global home_bench
        home_bench = home_t
        global away_bench
        away_bench = away_t
        # print(home_bench)
        # update field
        return player_pos

    @app.callback(
        Output(radar_plot.html_id, "figure"),
        [
            Input("radar-button", "n_clicks"),
            Input("select-button", "n_clicks"),
        ],
    )
    # just to make it listen
    def update_radar(rad_button, select_but):
        return radar_plot.plot_radar(selected_players)

    @app.callback(
        Output(historic_plot.html_id, "figure"),
        [Input("home-dropdown", "value"), Input("away-dropdown", "value")],
    )
    def update_historic(home, away):
        return historic_plot.build_historic(home, away)

    @app.callback(
        Output(team_plot.html_id, "figure"),
        [
            Input("home-dropdown", "value"),  # home team
            Input("away-dropdown", "value"),
        ],  # away team
    )
    def update_team_plot(home_team, away_team):
        selected_teams = [home_team, away_team]

        # dealy needed in order to ensure that the filed is updated
        time.sleep(1)

        return team_plot.plot_bar(features, selected_teams, all_players)

    @app.callback(
        Output("table_out_home", "children"),
        [
            Input("home-dropdown", "value"),
        ],
    )
    def update_table(home_drop):
        # dealy needed in order to ensure that the filed is updated
        time.sleep(1)
        return home_table.plot_table(home_bench)

    @app.callback(
        Output("table_out_home_high", "children"),
        [
            Input(home_table.html_id, "active_cell"),
        ],
    )
    def update_graph_home(active_cell):
        # print("triggereed")
        if active_cell:
            # print("inside")
            cell_data = home_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            return f'Data: "{cell_data}" from table cell: {active_cell}'
        return "Click the Players to Swap"

    # **********************************
    @app.callback(
        Output("table_out_away", "children"),
        [
            Input("away-dropdown", "value"),
        ],
    )
    def update_table(away_drop):
        # dealy needed in order to ensure that the filed is updated
        time.sleep(1)
        return away_table.plot_table(away_bench)

    @app.callback(
        Output("table_out_away_high", "children"),
        [
            Input(away_table.html_id, "active_cell"),
        ],
    )
    def update_graph_away(active_cell):
        # print("triggereed")
        if active_cell:
            # print("inside")
            cell_data = away_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            return f'Data: "{cell_data}" from table cell: {active_cell}'
        return "Click the Players to Swap"

    app.run_server(debug=False, dev_tools_ui=False)
