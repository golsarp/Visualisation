from jbi100_app.main import app
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.field import Field
from jbi100_app.views.radar_plot import Radar
from jbi100_app.views.team_plot import Bar
import time
from jbi100_app.views.historic import Historic
from jbi100_app.views.table import Table
from dash import callback_context


# import dash_core_components as dcc
from dash import dcc
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
    formation,
    swap_players,
)


from dash import html, Dash, no_update
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

    selected_players_team_plot_field = []

    sorted_features = []
    # to swap bench players
    home_swap = False
    home_selected_field = None
    home_selected_bench = None

    # to swap away bench
    away_swap = False
    away_selected_field = None
    away_selected_bench = None

    player_dataf = None

    # Field object
    field = Field("Footbal Field", "x", "y")

    # radar plot
    radar_plot = Radar("Radar-plot", selected_players)
    # historical plot
    historic_plot = Historic("Historic-plot")

    home_bench = None

    home_table = Table("home-table")

    away_table = Table("away-table")
    away_bench = None

    # first 5 teams initially
    # there are 32 teams, idk how to display them nicely
    df = pd.read_csv(player_poss_path)
    teams = df["team"].unique()[:20]

    l = ["a", "b"]

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
                                style={
                                    "display": "inline-block",
                                    "width": "25%",
                                },
                                # style={"display": "flex", "width": "25%"},
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
                                # style={"display": "flex", "width": "25%"},
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
                                # style={"display": "flex", "width": "25%"},
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
                                # style={"display": "flex", "width": "25%"},
                            ),
                        ],
                        # style={"display": "flex", "flexWrap": "wrap"},
                    ),
                    # Existing components
                    # field object
                    field,
                    html.Div(
                        [
                            html.Div(
                                [
                                    # html.H4("Home Bench"),
                                    html.P(id="table_out_home"),
                                    html.P(id="table_out_home_high"),
                                    ################# home bench ##########
                                    html.Button(
                                        "Swap Home Off ", id="home-swap", n_clicks=0
                                    ),
                                    # use this to update the field
                                    html.Button(
                                        "Swap",
                                        id="home-swap_players",
                                        n_clicks=0,
                                    ),
                                    # home_table,
                                ],
                                # html.Button("Swap Home ", id="home-swap", n_clicks=0),
                                style={
                                    "display": "inline-block",
                                    "width": "30%",
                                    "margin-right": "50px",  # Add margin to the right
                                },
                            ),
                            html.Div(
                                [
                                    # html.H4("Away Bench"),
                                    html.P(id="table_out_away"),
                                    html.P(id="table_out_away_high"),
                                    html.Button(
                                        "Swap Away Off ", id="away-swap", n_clicks=0
                                    ),
                                    html.Button(
                                        "Swap",
                                        id="away-swap_players",
                                        n_clicks=0,
                                    ),
                                    # home_table,
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "30%",
                                },
                            ),
                            html.Div(
                                [
                                    radar_plot,
                                    html.Button(
                                        "Plot button", id="radar-button", n_clicks=0
                                    ),
                                    html.Button(
                                        children="Select Players Off",
                                        id="select-button",
                                        n_clicks=0,
                                    ),
                                ],
                                style={
                                    "display": "inline-block",
                                    # "width": "30%",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                        },
                    ),
                    dcc.Tabs(
                        id="my-tabs",
                        value="tab1",
                        children=[
                            dcc.Tab(label="Category 1", value="tab1"),
                            dcc.Tab(label="Category 2", value=l),
                            dcc.Tab(label="Category 3", value="tab3"),
                        ],
                        style={
                            "fontSize": 12,  # Adjust the font size
                            "height": 30,  # Adjust the height
                            "padding": "5px",  # Adjust padding
                        },
                    ),
                    html.Div(id="hidden-div", style={"display": "none"}),
                ],
            ),
            html.Div(
                id="right-column",
                className="four columns",
                children=[
                    # radar plot
                    # radar_plot,
                    # html.Button("Plot button", id="radar-button", n_clicks=0),
                    # html.Button(
                    #     children="Select Players Off",
                    #     id="select-button",
                    #     n_clicks=0,
                    # ),
                    # team plot
                    team_plot,
                    dcc.Store(id="team-plot-store", data={}),
                    dcc.Store(id="filtered_stored_data", data={}),
                    # team plot dropdown feature selector
                    dcc.Dropdown(
                        [
                            "dribbles_completed",
                            "passes_short",
                            "passes_medium",
                            "passes_long",
                            "shots_on_target",
                        ],
                        ["dribbles_completed", "shots_on_target"],
                        multi=True,
                        id="team-plot-dropdown",
                    ),
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
            Input("select-button", "n_clicks"),
            Input("home-swap_players", "n_clicks"),
            Input("away-swap_players", "n_clicks"),
        ],
    )
    def update_field(
        select,
        click_data,
        home,
        away,
        home_form,
        away_from,
        select_button,
        swap_home_but,
        swap_away_but,
    ):
        triggered_input_id = callback_context.triggered_id
        # get selected players
        global home_selected_field
        global home_selected_bench
        # for away bench
        global away_selected_field
        global away_selected_bench
        global player_dataf
        global home_bench
        global away_bench

        if click_data is not None:
            # Extract information about the clicked point
            clicked_point_info = click_data["points"][0]
            clicked_name = clicked_point_info["customdata"][0]
            # we are selecting for radar plot
            if player_select and not home_swap and not away_swap:
                if clicked_name in selected_players:
                    selected_players.remove(clicked_name)
                else:
                    selected_players.append(clicked_name)
            # selecting for bench player swap
            elif not player_select and home_swap:
                # print("here ")
                # check if its in home team
                in_team = (player_dataf["player"] == clicked_name) & (
                    player_dataf["team"] == home
                )
                if clicked_name not in selected_players and in_team.any():
                    home_selected_field = clicked_name
                # print(home_selected_field)

            # for selecting away players
            elif not player_select and away_swap:
                # print("away selection ")
                # check if its in home team
                in_team = (player_dataf["player"] == clicked_name) & (
                    player_dataf["team"] == away
                )
                if clicked_name not in selected_players and in_team.any():
                    away_selected_field = clicked_name
                # print(away_selected_field)

        # print("click", click_data)
        # print("swap", swap_home_but)

        # players changed make them null so we update in field
        if (
            triggered_input_id == "home-dropdown"
            or triggered_input_id == "away-dropdown"
            or triggered_input_id == "home-formation"
            or triggered_input_id == "away-formation"
        ):
            # print("made it none ")
            # print(triggered_input_id)
            player_dataf = None
            home_bench = None
            away_bench = None

        if triggered_input_id == "home-swap_players":
            if home_selected_bench is not None and home_selected_field is not None:
                player_dataf, home_bench = swap_players(
                    home_selected_field,
                    home_selected_bench,
                    home_bench=home_bench,
                    player_dataf=player_dataf,
                )
                home_selected_bench = None
                home_selected_field = None

        if triggered_input_id == "away-swap_players":
            # print("Entered here ")
            if away_selected_bench is not None and away_selected_field is not None:
                player_dataf, away_bench = swap_players(
                    away_selected_field,
                    away_selected_bench,
                    home_bench=away_bench,
                    player_dataf=player_dataf,
                )
                away_selected_bench = None
                away_selected_field = None

        # update field with globals
        player_pos, player_df, home_t, away_t = field.positionPlayer(
            home,
            away,
            home_form,
            away_from,
            selected_players=selected_players,
            home_field_pl=home_selected_field,
            away_field_pl=away_selected_field,
            df_concat=player_dataf,
            home_table=home_bench,
            away_table=away_bench,
        )

        player_dataf = player_df

        global all_players
        # all_players = player_df["player"].unique()
        all_players = player_dataf["player"].unique()

        # for tables

        home_bench = home_t

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
        Output("team-plot-store", "data"),
        Input(team_plot.html_id, "clickData"),
        State("team-plot-store", "data"),
        Input("home-dropdown", "value"),  # home team
        Input("away-dropdown", "value"),  # away team
    )
    def store_click_data(click_data, stored_data, home_team, away_team):
        # if no point has been clicked yet or the teams have changed, initialize an empty list
        if click_data is None:
            return []

        # check if stored data has values
        if stored_data:
            # Check if the teams in stored_data are the same as the input teams
            stored_teams = {segment.split('|')[0] for segment in stored_data}
            if home_team not in stored_teams and away_team not in stored_teams:
                return []

        # TODO: remove players from stored_data if they are not in selected_players_team_plot_field. Select players
        #  in all features if they have been selected in selected_players_team_plot_field

        global sorted_features

        # which point has been clicked?
        clicked_point = click_data["points"][0]["pointIndex"]
        clicked_team_index = click_data["points"][0]["curveNumber"]

        # determine the team name based on the clicked_team_index
        team_name = home_team if clicked_team_index == 0 else away_team

        if clicked_point < 11:
            stack_index = clicked_point
            feature_index = 0
        else:
            stack_index = clicked_point % 11
            feature_index = clicked_point // 11

        # determine the feature name based on the feature_index
        feature_name = sorted_features[feature_index]

        # get the dataframe of players on the field.
        sorted_plot_df = team_plot.get_dataframe()

        filtered_df = sorted_plot_df[(sorted_plot_df['team'] == team_name)
                                     & (sorted_plot_df['feature'] == feature_name)]
        # Reset the index of the dataframe
        filtered_df = filtered_df.reset_index(drop=True)
        # Get the player's name at the feature_index
        player_name = filtered_df.loc[stack_index, 'name']

        # create a unique key for the clicked segment
        clicked_segment = f"{team_name}|{feature_name}|{stack_index}|{player_name}"

        # if the clicked segment is already selected, deselect it
        if clicked_segment in stored_data:
            stored_data.remove(clicked_segment)
        # otherwise, select the clicked segment
        else:
            stored_data.append(clicked_segment)

        global selected_players_team_plot_field

        selected_players_team_plot_field = []

        # Iterate over each segment in stored_data
        for segment in stored_data:
            # Split the segment string into parts
            parts = segment.split("|")
            # The player name is the last part
            player_name = parts[-1]

            # Add players to selected_players_team_plot_field if they are not already in it
            if player_name not in selected_players_team_plot_field:
                selected_players_team_plot_field.append(player_name)

        return stored_data

    @app.callback(
        Output(team_plot.html_id, "figure"),
        [
            Input("home-dropdown", "value"),  # home team
            Input("away-dropdown", "value"),  # away team
            Input("home-formation", "value"),
            Input("away-formation", "value"),
            Input("team-plot-dropdown", "value"),  # feature selection
            Input("team-plot-store", "data"),
            Input("home-swap_players", "n_clicks"),
            Input("away-swap_players", "n_clicks"),
        ],
    )
    def update_team_plot(home_team, away_team, features, stored_data_transfer,swap_home,
        swap_away):
        # delay needed in order to ensure that the filed is updated
        time.sleep(1)

        # TODO: deselect selection for features which are no longer used (use optional callback output)

        filtered_stored_data_transfer = [entry for entry in stored_data_transfer if
                                         any(feature in entry for feature in features)]

        global sorted_features
        sorted_features = sorted(features)

        # update the figure with the new data
        updated_figure = team_plot.plot_bar(sorted_features, all_players)

        # extract traces
        traces = updated_figure["data"]

        playing_teams = [home_team, away_team]

        stored_data = {}
        for segment in filtered_stored_data_transfer:
            team_name, feature_name, stack_index, _ = segment.split('|')
            team_index = str(playing_teams.index(team_name))
            feature_index = sorted_features.index(feature_name)
            clicked_point = feature_index * 11 + int(stack_index)
            if team_index not in stored_data:
                stored_data[team_index] = []
            stored_data[team_index].append(clicked_point)

        # if stored_data is not initialized yet, initialize it with all points selected.
        # If stored data is empty, initialize it with all points selected
        if not stored_data or (
            len(stored_data) == 1 and not next(iter(stored_data.values()))
        ):
            stored_data = {
                str(i): list(range(len(trace["y"])))
                for i, trace in enumerate(updated_figure["data"])
            }

        # loop over all traces
        for idx, trace in enumerate(traces):
            # update selection state of the clicked point in the trace dict
            if str(idx) in stored_data:
                trace.update({"selectedpoints": stored_data[str(idx)]})
            else:
                trace.update({"selectedpoints": []})

            # update figure dict with updated trace dict
            updated_figure["data"][idx].update(trace)

        return updated_figure

    # bench for home

    @app.callback(
        Output("table_out_home", "children"),
        [
            Input("home-dropdown", "value"),
            Input("home-formation", "value"),
            Input("home-swap_players", "n_clicks"),
        ],
    )
    def update_table(home_drop, home_form, swap):
        # dealy needed in order to ensure that the filed is updated
        time.sleep(1)
        # print(home_bench.columns)
        return home_table.plot_table(home_bench)

    @app.callback(
        Output("table_out_home_high", "children"),
        [
            Input(home_table.html_id, "active_cell"),
        ],
    )
    def update_graph_home(active_cell):
        global home_selected_bench
        # print("triggereed")
        if active_cell:
            # print("inside")
            cell_data = home_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            # print(f'Data: "{cell_data}" from table cell: {active_cell}')
            home_selected_bench = cell_data
            if not home_swap:
                # print("Added from home bench")
                selected_players.append(cell_data)
            # print("home bench ", home_selected_bench)

            # return f'Data: "{cell_data}" from table cell: {active_cell}'
        # return "Click the Players to Swap"

    # **********************************
    # bench for away
    @app.callback(
        Output("table_out_away", "children"),
        [
            Input("away-dropdown", "value"),
            Input("away-formation", "value"),
            Input("away-swap_players", "n_clicks"),
        ],
    )
    def update_table(away_drop, away_from, swap_away):
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
        global away_selected_bench
        if active_cell:
            # print("inside")
            cell_data = away_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            away_selected_bench = cell_data

            # add to radar plot from away bench
            if not away_swap:
                # print("Added from bench")
                selected_players.append(cell_data)

            # print(f'Data: "{cell_data}" from table cell: {active_cell}')
            # return f'Data: "{cell_data}" from table cell: {active_cell}'
        # return "Click the Players to Swap"

    ########################## Swapping bench players #####################
    @app.callback(
        Output("home-swap", "children"),
        [Input("home-swap", "n_clicks")],
    )
    def update_output(n_clicks):
        # global used for player selection
        global home_swap
        global home_selected_bench
        global home_selected_field

        if n_clicks % 2 == 1:
            new_label = "Reset"
            home_swap = True
            return new_label
        else:
            home_swap = False
            # open if you want to update it
            home_selected_field = None
            new_label = "Select"
            return new_label

    @app.callback(
        Output("away-swap", "children"),
        [Input("away-swap", "n_clicks")],
    )
    def update_output(n_clicks):
        # global used for player selection
        global away_swap
        global away_selected_bench
        global away_selected_field

        if n_clicks % 2 == 1:
            new_label = "Reset"
            away_swap = True
            return new_label
        else:
            away_swap = False
            # open if you want to update it
            away_selected_field = None
            new_label = "Select"
            return new_label

        # Callback to update the content based on the selected tab

    @app.callback(Output("hidden-div", "children"), [Input("my-tabs", "value")])
    def update_output(selected_tab):
        print("tab: ", selected_tab)
        return f"The selected category is: {selected_tab}"

    app.run_server(debug=False, dev_tools_ui=False)
