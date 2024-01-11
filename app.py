from jbi100_app.main import app
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field
from jbi100_app.views.radar_plot import Radar
from jbi100_app.views.team_plot import Bar
import time
from jbi100_app.views.historic import Historic

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
    # clicked players, initially set to some players
    selected_players = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]

    all_players = ["Aaron Mooy", "Aaron Ramsey", "Brennan Johnson"]

    # selected teams
    selected_teams = ["Australia", "Wales"]

    # team features
    features = ["dribbles_completed", "passes_short", "shots_on_target"]

    # If selection is on
    player_select = False

    # Field object
    field = Field("Footbal Field", "x", "y")

    # radar plot
    radar_plot = Radar("Radar-plot", selected_players)
    #historical plot
    historic_plot = Historic("Historic-plot")
   
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
                    # team plot dropdown feature selector
                    dcc.Dropdown(['dribbles_completed', 'passes_short', 'passes_medium',
                                  'passes_long', 'shots_on_target'],
                                 ['dribbles_completed', 'shots_on_target'],
                                 multi=True, id="team-plot-dropdown"),
                    # historic plot
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

        player_pos, player_df = field.positionPlayer(home, away, home_form, away_from)

        global all_players
        all_players = player_df["player"].unique()

        # update field
        return player_pos

    @app.callback(
        Output(radar_plot.html_id, "figure"),
        [Input("radar-button", "n_clicks"),
         Input("select-button", "n_clicks"),],
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
        [Input("home-dropdown", "value"),   # home team
         Input("away-dropdown", "value"),  # away team
         Input("team-plot-dropdown", "value"),  # feature selection
         Input(team_plot.html_id, 'clickData')],  # click data
         State(team_plot.html_id, 'figure'),
        prevent_initial_call=True
    )
    def update_team_plot(home_team, away_team, features, click_data, current_figure):

        selected_teams = [home_team, away_team]

        # delay needed in order to ensure that the filed is updated
        time.sleep(1)

        updated_figure = team_plot.plot_bar(features, all_players)

        # if a segment of the bar chart was clicked
        if click_data is not None:
            # which point has been clicked?
            clicked_point = click_data["points"][0]["pointIndex"]
            clicked_trace = click_data["points"][0]["curveNumber"]

            # extract traces
            traces = updated_figure['data']

            # loop over all traces
            for idx, trace in enumerate(traces):
                # update selection state of the clicked point in the trace dict

                if idx == clicked_trace:
                    trace.update({'selectedpoints': [clicked_point]})
                else:
                    trace.update({'selectedpoints': []})

                    # update figure dict with updated trace dict
                updated_figure['data'][idx].update(trace)

        return updated_figure

    app.run_server(debug=False, dev_tools_ui=False)
