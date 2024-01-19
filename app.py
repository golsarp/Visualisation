import plotly.graph_objects as go
from jbi100_app.main import app
from jbi100_app.views.field import Field
from jbi100_app.views.radar_plot import Radar
from jbi100_app.views.team_plot import Bar
import time
from jbi100_app.views.historic import Historic
from jbi100_app.views.table import Table
from dash import callback_context


from dash import dcc
from jbi100_app.config import (
    player_poss_path,
    formation,
    swap_players,
    color_list,
    color_red_blind,
    color_list_random,
)


from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd

if __name__ == "__main__":

    selected_players_team_plot_field = []

    sum_correlation = False

    updated_stacked_bar = False

    home_form_bar = '4-3-3-1'

    away_form_bar = '4-3-3-1'

    swap_home_bar = 0

    swap_away_bar = 0

    sorted_features = []

    bar_chart_teams = ["Australia", "Wales"]

    bar_chart_teams_plot = ["Australia", "Wales"]

    global_features = ["dribbles_completed", "shots_on_target"]
    # clicked players, initially set to some players
    selected_players = ["Mathew Leckie", "Joe Allen", "Ben Davies"]

    all_players = ["Aaron Mooy", "Aaron Ramsey", "Brennan Johnson"]

    # selected teams
    selected_teams = ["Australia", "Wales"]

    # team features
    features = ["dribbles_completed", "passes_short", "shots_on_target"]

    # If selection is on
    player_select = False

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

    df = pd.read_csv(player_poss_path)
    teams = df["team"].unique()

    app_color = color_list

    # team plot
    team_plot = Bar("Team-plot", selected_players, selected_teams, features)

    column_name_to_alias = {
        "dribbles_completed": "Dribbles",
        "passes_short": "Short",
        "passes_medium": "Medium",
        "passes_long": "Long",
        "shots_on_target": "Shots",
        "goals": "Goals",
    }

    # Generate the options for the dropdown using the dictionary
    options = [{"label": alias, "value": column_name} for column_name, alias in column_name_to_alias.items()]

    # Define the layout
    app.layout = html.Div(
       

        id="app-container",
        children=[
            dcc.ConfirmDialog(
                id="popup-message",
                message=(
                    "This is your pop-up message to help you use the app.\n\n"
                    "• To swap players from the field and bench, use Select and Swap buttons under the tables.\n"
                    "• To compare players, use the Select and Plot buttons under the Radar plot.\n"
                    "• Selected players will also be highlighted in the Team plot Bar chart.\n"
                    "• To reconfigure bar chart, use the % or ∑ under the Radar Plot.\n"
                    "• To further compare teams, feel free to change formations using the buttons on top of the Field.\n\n"
                    "• All plots will be updated accordingly after changing teams or formations.\n\n"
                    "• Please wait while the app is updating. You can check this from the tab ribbon.\n\n"
                    "• For a demonstration and further explanation a feel free to visit our Github: https://github.com/golsarp/Visualisation .\n\n"
    
                    "Enjoy the app!!"
                ),
                displayed=True,  # Show the message initially
            ),
            
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
                                    # html.H4("Home Bench"),
                                    html.P(id="table_out_home"),
                                    html.P(id="table_out_home_high"),
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
                                    html.Button(id="sum-per", n_clicks=0),
                                ],
                                style={
                                    "display": "inline-block",
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
                            dcc.Tab(label="Normal Colors", value="tab1"),
                            dcc.Tab(label="Deuteranamoly", value="tab2"),

                            dcc.Tab(label="Protanopia", value="tab3"),
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
                    # team plot
                    team_plot,
                    dcc.Store(id="team-plot-store", data={}),
                    # team plot dropdown feature selector
                    dcc.Dropdown(
                        options=options,
                        value=["dribbles_completed", "shots_on_target"],  # Initial selected values
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
            Input("my-tabs", "value"),
            Input("team-plot-store", "data"),
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
        color,
        bar,
    ):

        time.sleep(0.4)

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
                # check if its in home team
                in_team = (player_dataf["player"] == clicked_name) & (
                    player_dataf["team"] == home
                )
                if clicked_name not in selected_players and in_team.any():
                    home_selected_field = clicked_name

            # for selecting away players
            elif not player_select and away_swap:
                # check if its in home team
                in_team = (player_dataf["player"] == clicked_name) & (
                    player_dataf["team"] == away
                )
                if clicked_name not in selected_players and in_team.any():
                    away_selected_field = clicked_name

        # players changed make them null so we update in field
        if (
            triggered_input_id == "home-dropdown"
            or triggered_input_id == "away-dropdown"
            or triggered_input_id == "home-formation"
            or triggered_input_id == "away-formation"
        ):

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
            colors=app_color,
            bar_players=selected_players_team_plot_field,
        )

        player_dataf = player_df

        global all_players
        all_players = player_dataf["player"].unique()

        # for tables

        home_bench = home_t

        away_bench = away_t
        # update field
        time.sleep(0.5)
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
        [
            Input("home-dropdown", "value"),
            Input("away-dropdown", "value"),
            Input("my-tabs", "value")],
    )
    def update_historic(home, away, color):
        time.sleep(0.2)
        return historic_plot.build_historic(home, away, app_color)

    @app.callback(
        Output("team-plot-store", "data"),
        Input(team_plot.html_id, "clickData"),
        State("team-plot-store", "data"),
        Input("home-dropdown", "value"),  # home team
        Input("away-dropdown", "value"),  # away team
        Input("team-plot-dropdown", "value"),
    )
    def store_click_data(click_data, stored_data, home_team, away_team, plot_features):

        global bar_chart_teams

        global selected_players_team_plot_field

        # Reset the selected_players_team_plot_field
        selected_players_team_plot_field = []

        # check if the teams have changed
        if home_team != bar_chart_teams[0] or away_team != bar_chart_teams[1]:
            bar_chart_teams = [home_team, away_team]
            return []

        global global_features

        # check if the features have changed
        if len(plot_features) != len(global_features):
            global_features = plot_features
            return []

        # if no point has been clicked yet, initialize an empty list
        if click_data is None:
            return []

        global sorted_features

        # check which segment has been clicked
        clicked_point = click_data["points"][0]["pointIndex"]

        # check which team has been clicked
        clicked_team_index = click_data["points"][0]["curveNumber"]

        # get the team name of the clicked segment
        plot_teams = [home_team, away_team]
        plot_teams.sort()
        team_name = plot_teams[clicked_team_index]

        # determine the player and feature which has been clicked
        if clicked_point < 11:
            stack_index = clicked_point
            feature_index = 0
        else:
            stack_index = clicked_point % 11
            feature_index = clicked_point // 11

        feature_alias = {
            "dribbles_completed": "Dribbles",
            "passes_short": "Short",
            "passes_medium": "Medium",
            "passes_long": "Long",
            "shots_on_target": "Shots",
            "goals": "Goals",
        }

        # determine the feature name based on the feature_index
        feature_name = sorted_features[feature_index]

        feature_name = feature_alias.get(feature_name, feature_name)

        # get the dataframe of players on the field.
        sorted_plot_df = team_plot.get_dataframe()

        # filter the dataframe based on the team and feature
        filtered_df = sorted_plot_df[(sorted_plot_df['team'] == team_name)
                                     & (sorted_plot_df['feature'] == feature_name)]

        # Reset the index of the dataframe
        filtered_df = filtered_df.reset_index(drop=True)

        # Get the player's name at the feature_index
        player_name = filtered_df.loc[stack_index, 'name']

        # create a unique key for the clicked segment
        clicked_segment = f"{team_name}|{feature_name}|{stack_index}|{player_name}"

        # if the clicked segment in stored_data is already selected, deselect it
        if clicked_segment in stored_data:
            stored_data.remove(clicked_segment)
        # otherwise, select the clicked segment
        else:
            stored_data.append(clicked_segment)

        # Iterate over each segment in stored_data to extract the player name
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
            State("team-plot-dropdown", "value"),  # feature selection
            Input("team-plot-store", "data"),
            Input("home-swap_players", "n_clicks"),
            Input("away-swap_players", "n_clicks"),
            Input("radar-button", "n_clicks"),
            Input("select-button", "n_clicks"),
            Input("sum-per", "children"),
            Input("my-tabs", "value")
        ],
    )
    def update_team_plot(home_team, away_team, home_form, away_from, features_param, stored_data_transfer, swap_home,
                         swap_away, highlight_button, reset_button, mode, color):

        # delay needed in order to ensure that the filed is updated
        time.sleep(1.0)

        global sorted_features
        sorted_features = sorted(features_param)

        global sum_correlation

        global updated_stacked_bar

        global bar_chart_teams_plot

        global home_form_bar

        global away_form_bar

        global swap_home_bar

        global swap_away_bar

        # Get the dataframe
        sorted_plot_df = team_plot.get_dataframe()

        if (
                sorted_plot_df is not None
                and sum_correlation is True
                and len(features_param) == sorted_plot_df['feature'].nunique()
                and home_team == bar_chart_teams_plot[0]
                and away_team == bar_chart_teams_plot[1]
                and home_form == home_form_bar
                and away_from == away_form_bar
                and swap_home == swap_home_bar
                and swap_away == swap_away_bar
        ):

            # Calculate the total value for each feature for each team
            total_values = sorted_plot_df.groupby(['team', 'feature'])['value'].sum()

            # Calculate the percentage contribution of each player for each feature
            sorted_plot_df['percentage'] = sorted_plot_df.apply(
                lambda row: (row['value'] / total_values[(row['team'], row['feature'])]) * 100, axis=1)

            # Drop the 'value' column
            sorted_plot_df = sorted_plot_df.drop(columns=['value'])

            # Rename the 'percentage' column to 'value'
            sorted_plot_df = sorted_plot_df.rename(columns={'percentage': 'value'})

            # Update the figure with the new data
            updated_figure = team_plot.plot_bar(sorted_features, all_players, app_color, home_team, away_team, sorted_plot_df)

        else:

            if sorted_plot_df is not None:
                if len(features_param) != sorted_plot_df['feature'].nunique():
                    updated_stacked_bar = True

            if home_team != bar_chart_teams_plot[0] or away_team != bar_chart_teams_plot[1]:
                updated_stacked_bar = True

            if home_form != home_form_bar or away_from != away_form_bar:
                updated_stacked_bar = True

            if swap_home != swap_home_bar or swap_away != swap_away_bar:
                updated_stacked_bar = True

            updated_figure = team_plot.plot_bar(sorted_features, all_players, app_color, home_team, away_team)

        bar_chart_teams_plot = [home_team, away_team]

        home_form_bar = home_form

        away_form_bar = away_from

        swap_home_bar = swap_home

        swap_away_bar = swap_away

        # extract traces
        traces = updated_figure["data"]

        global selected_players

        playing_teams_unsorted = [home_team, away_team]

        playing_teams = sorted(playing_teams_unsorted)

        feature_alias = {
            "Dribbles": "dribbles_completed",
            "Short": "passes_short",
            "Medium": "passes_medium",
            "Long": "passes_long",
            "Shots": "shots_on_target",
            "Goals": "goals",
        }

        stored_data = {}
        for segment in stored_data_transfer:
            team_name, feature_name, stack_index, _ = segment.split('|')
            team_index = str(playing_teams.index(team_name))
            feature_name = feature_alias.get(feature_name, feature_name)
            feature_index = sorted_features.index(feature_name)
            clicked_point = feature_index * 11 + int(stack_index)
            if team_index not in stored_data:
                stored_data[team_index] = []
            stored_data[team_index].append(clicked_point)

        if not stored_data or (
            len(stored_data) == 1 and not next(iter(stored_data.values()))
        ):
            stored_data = {
                str(i): list(range(len(trace["y"])))
                for i, trace in enumerate(updated_figure["data"])
            }

        # loop over all traces
        for idx, trace in enumerate(traces):

            # get the player's name from the trace's custom data
            player_names = [data[0] for data in trace['customdata']]
            team_names = [data[1] for data in trace['customdata']]

            team_indices = [playing_teams.index(team_name) for team_name in team_names]

            if playing_teams_unsorted == playing_teams:
                # create a list of colors for each bar in the trace
                colors = [app_color[5] if player_name in selected_players
                          else (app_color[0] if int(team_index) == 0 else app_color[1]) for
                          player_name, team_index in zip(player_names, team_indices)]
            else:
                colors = [app_color[5] if player_name in selected_players
                          else (app_color[1] if int(team_index) == 0 else app_color[0]) for
                          player_name, team_index in zip(player_names, team_indices)]

            # update the trace's color
            trace['marker']['color'] = colors

            # update selection state of the clicked point in the trace dict
            if str(idx) in stored_data:
                trace.update({"selectedpoints": stored_data[str(idx)]})
            else:
                trace.update({"selectedpoints": []})

            # update figure dict with updated trace dict
            updated_figure["data"][idx].update(trace)

        if playing_teams_unsorted == playing_teams:
            # Customize legend labels for specific colors
            legend_labels = {'rgb(255,0,0)': home_team, 'rgb(0,255,0)': away_team, 'rgb(255,255,0)': 'Selected Players'}
            for trace, legend_label in zip(updated_figure.data, legend_labels.values()):
                trace.name = legend_label

        else:
            legend_labels = {'rgb(255,0,0)': away_team, 'rgb(0,255,0)': home_team, 'rgb(255,255,0)': 'Selected Players'}
            for trace, legend_label in zip(updated_figure.data, legend_labels.values()):
                trace.name = legend_label

        # Add a dummy trace for the yellow color
        updated_figure.add_trace(go.Bar(x=[None], y=[None], marker_color='rgb(255,255,0)', name='Selected Players'))

        return updated_figure

    @app.callback(
        Output("sum-per", "children"),
        [Input("sum-per", "n_clicks"),
         Input(team_plot.html_id, "figure")],
    )
    def update_output(n_clicks, fig):
        # global used for player selection
        global sum_correlation
        global updated_stacked_bar

        if updated_stacked_bar:
            updated_stacked_bar = False
            sum_correlation = False
            new_label = "%"
            return new_label

        if n_clicks % 2 == 1:
            new_label = "∑"
            sum_correlation = True
            return new_label
        else:
            sum_correlation = False
            new_label = "%"
            return new_label

    @app.callback(
        Output("table_out_home", "children"),
        [
            Input("home-dropdown", "value"),
            Input("home-formation", "value"),
            Input("home-swap_players", "n_clicks"),
            Input("my-tabs", "value")
        ],
    )
    def update_table(home_drop, home_form, swap, color):
        # dealy needed in order to ensure that the filed is updated
        time.sleep(1.5)
        return home_table.plot_table(home_bench, home=True, colors=app_color)

    @app.callback(
        Output("table_out_home_high", "children"),
        [
            Input(home_table.html_id, "active_cell"),
        ],
    )
    def update_graph_home(active_cell):
        time.sleep(1.0)
        global home_selected_bench
        if active_cell:
            cell_data = home_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            home_selected_bench = cell_data
            if not home_swap:
                selected_players.append(cell_data)

    # **********************************
    # bench for away
    @app.callback(
        Output("table_out_away", "children"),
        [
            Input("away-dropdown", "value"),
            Input("away-formation", "value"),
            Input("away-swap_players", "n_clicks"),
            Input("my-tabs", "value"),
        ],
    )
    def update_table(away_drop, away_from, swap_away, color):
        # dealy needed in order to ensure that the filed is updated

        time.sleep(1.5)
        return away_table.plot_table(away_bench, home=False, colors=app_color)

    @app.callback(
        Output("table_out_away_high", "children"),
        [
            Input(away_table.html_id, "active_cell"),
        ],
    )
    def update_graph_away(active_cell):
        time.sleep(1.0)
        global away_selected_bench
        if active_cell:
            cell_data = away_bench.iloc[active_cell["row"]][active_cell["column_id"]]
            away_selected_bench = cell_data

            # add to radar plot from away bench
            if not away_swap:
                selected_players.append(cell_data)

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
        global app_color

        # You can add more logic based on the selected_tab value if needed
        if selected_tab == "tab1":
            app_color = color_list
        elif selected_tab == "tab2":
            app_color = color_red_blind
        elif selected_tab == "tab3":
            app_color = color_list_random
        time.sleep(1.0)
        return f"The selected category is: {selected_tab}"
    

    app.run_server(debug=False, dev_tools_ui=False)
