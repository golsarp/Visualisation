from dash import dcc, html
import plotly.express as px
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
)

import pandas as pd


class Field(html.Div):
    def __init__(self, name, feature_x, feature_y):
        self.html_id = name.lower().replace(" ", "-")

        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def select_players(self, df, formation):
        """
        This method is used to select players for a given formation from a DataFrame.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the player data.
        formation (str): The formation to be used, represented as a string of numbers separated by dashes ("-").

        Returns:
        selected_players (pandas.DataFrame): A DataFrame containing the players selected for the formation.
        bench_players (pandas.DataFrame): A DataFrame containing the players not selected for the formation (i.e., the bench players).
        """

        # Split the formation string into a list of strings
        positions = formation.split("-")
        # Convert the list of strings into a list of integers
        positions = list(map(int, positions))
        # Initialize an empty DataFrame for the selected players
        selected_players = pd.DataFrame()
        # Initialize an empty DataFrame for the bench players
        bench_players = pd.DataFrame()

        # Initialize a counter
        i = 0
        # Iterate over the positions in the formation
        for pos in positions:
            # Select the players from the DataFrame whose position starts with the appropriate string
            position_df = df[
                df["position"].str.startswith(
                    "FW" if i == 0 else "MF" if i == 1 else "DF" if i == 2 else "GK"
                )
            ]
            # Add the first 'pos' players from the position DataFrame to the selected players DataFrame
            selected_players = pd.concat([selected_players, position_df.head(pos)])
            # Add the remaining players from the position DataFrame to the bench players DataFrame
            bench_players = pd.concat([bench_players, position_df.tail(-pos)])

            # Increment the counter
            i += 1

        # Return the selected players and bench players DataFrames
        return selected_players, bench_players

    def process_df(self, team, home):
        """
        This method processes the DataFrame of player positions for a given team.

        Parameters:
        team (str): The team for which the DataFrame is to be processed.
        home (bool): A boolean indicating whether the team is playing at home or not.

        Returns:
        df_team (pandas.DataFrame): A DataFrame containing the processed player positions for the team.
        """

        # Read the player positions data from the CSV file
        df = pd.read_csv(player_poss_path)
        # Filter the DataFrame to only include rows for the specified team
        df_team = df[df["team"] == team].copy()
        # Sort the DataFrame by the 'position' column
        df_team = df_team.sort_values(by="position")
        # Determine the mapping to be used based on whether the team is playing at home or not
        mapping = position_mapping_home if home else position_mapping_away

        # Map the 'position' column of the DataFrame using the determined mapping
        df_team["position_x"] = df_team["position"].map(mapping)
        # Assign a cumulative count of each position to the 'position_y' column of the DataFrame
        df_team["position_y"] = df_team.groupby("position").cumcount() + 1

        # Return the processed DataFrame
        return df_team

    def calculate_corrected_y(self, group, max_val):
        """
        This method calculates the corrected y-coordinate for each player in a group.

        Parameters:
        group (pandas.DataFrame): The DataFrame containing the player data for a specific position.
        max_val (int): The maximum y-coordinate value among all positions.

        Returns:
        corrected_y (pandas.Series): A Series containing the corrected y-coordinates for the players in the group.
        """

        # Calculate the factor based on the maximum y-coordinate value and the number of players in the group
        factor = max_val / (len(group) + 1)

        # Calculate the corrected y-coordinate for each player in the group
        group["corrected_y"] = group["position_y"] * factor

        # Return the Series containing the corrected y-coordinates
        return group["corrected_y"]

    def positionPlayer(
        self,
        home,
        away,
        home_form,
        away_form,
        selected_players,
        home_field_pl,
        away_field_pl,
        df_concat,
        home_table,
        away_table,
        colors,
        bar_players,
    ):
        """
        This method is used to position players on a football field plot.

        Parameters:
        home (str): The home team name.
        away (str): The away team name.
        home_form (str): The formation of the home team.
        away_form (str): The formation of the away team.
        selected_players (list): List of selected players.
        home_field_pl (str): The player from the home team who is on the field.
        away_field_pl (str): The player from the away team who is on the field.
        df_concat (pandas.DataFrame): The DataFrame containing the player data for both teams.
        home_table (pandas.DataFrame): The DataFrame containing the player data for the home team.
        away_table (pandas.DataFrame): The DataFrame containing the player data for the away team.
        colors (list): List of colors to be used in the plot.
        bar_players (list): List of players who are on the bar.

        Returns:
        fig (plotly.graph_objs._figure.Figure): The figure containing the football field plot.
        df_concat (pandas.DataFrame): The DataFrame containing the player data for both teams.
        home_table (pandas.DataFrame): The DataFrame containing the player data for the home team.
        away_table (pandas.DataFrame): The DataFrame containing the player data for the away team.
        """

        # If df_concat is None, process the player data for both teams and select the players for the formations
        if df_concat is None:

            df_home = self.process_df(home, True)
            df_away = self.process_df(away, False)

            df_home_field, df_home_bench = self.select_players(df_home, home_form)

            df_away_field, df_away_bench = self.select_players(df_away, away_form)

            home_table = df_home_bench
            away_table = df_away_bench

            max_val_home = df_home_field["position_y"].max()
            max_val_away = df_away_field["position_y"].max()
            max_val = max(max_val_home, max_val_away)

            df_home_field["corrected_y"] = (
                df_home_field.groupby("position")
                .apply(lambda group: self.calculate_corrected_y(group, max_val))
                .reset_index(level=0, drop=True)
            )

            df_away_field["corrected_y"] = (
                df_away_field.groupby("position")
                .apply(lambda group: self.calculate_corrected_y(group, max_val))
                .reset_index(level=0, drop=True)
            )

            df_concat = pd.concat([df_home_field, df_away_field], ignore_index=True)

        # Assign colors to the players based on their team and whether they are on the field, on the bench, or selected
        df_concat["color"] = df_concat.apply(
            lambda row: colors[7]
            if row["player"] == away_field_pl
            else colors[7]
            if row["player"] == home_field_pl
            else colors[5]
            if row["player"] in selected_players
            else colors[5]
            if row["player"] in bar_players
            else colors[0]
            if row["team"] == home
            else colors[1]
            if row["team"] == away
            else "Other",
            axis=1,
        )

        # Define the columns to be displayed when hovering over the points in the plot
        hover_columns = [
            "player",
            "age",
            "minutes_90s",
            "miscontrols"
        ]

        # Define the mapping of colors to their corresponding values
        color_mapping = {
            colors[2]: colors[2],
            colors[0]: colors[0],
            colors[1]: colors[1],
            colors[5]: colors[5],
            colors[3]: colors[3],
            colors[4]: colors[4],
            colors[7]: colors[7],
            colors[14]: colors[14],
        }

        # Create the scatter plot
        self.fig = px.scatter(
            df_concat,
            y="corrected_y",
            x="position_x",
            color="color",
            symbol="position",
            hover_data=hover_columns,
            height=370,  # Set the height of the figure
            width=900,
            color_discrete_map=color_mapping,
        )

        # Define the mapping of symbols to their corresponding positions
        symbol_to_position = {
            'circle': 'FW',
            'diamond': 'MF',
            'square': 'DF',
            'x': 'GK'
        }

        # Create a dictionary that maps colors to teams
        color_to_team = df_concat.set_index('color')['team'].to_dict()

        # Set the name attribute for each trace
        self.fig.for_each_trace(
            lambda trace: trace.update(
                name=f"{symbol_to_position[trace.marker.symbol]}, {color_to_team[trace.marker.color]}")
        )

        # Define the list of colors
        color_list = [colors[0], colors[1], colors[5], colors[3], colors[4], colors[7], colors[14]]

        # Remove the color value from the hover template for each trace
        for color_value in color_list:
            self.fig.for_each_trace(
                lambda trace: trace.update(hovertemplate=trace.hovertemplate.replace(f'color={color_value}<br>', ''))
            )

        # Update the layout of the figure
        self.fig.update_layout(
            legend={"title": "Position, Team"},
            margin=dict(l=20, r=20, t=10, b=0),
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor=colors[2],
        )
        self.fig.update_xaxes(showticklabels=False)
        self.fig.update_yaxes(showticklabels=False)
        self.fig.update_xaxes(showgrid=True, gridcolor=colors[6])
        self.fig.update_yaxes(showgrid=True, gridcolor=colors[6])

        # Add annotations (text on top of values)
        for i, row in df_concat.iterrows():
            player_name_parts = row["player"].split()  # Split the full name into parts
            last_name = None
            # Use only the first part of the name
            if len(player_name_parts) > 1:
                last_name = player_name_parts[1] if player_name_parts else ""
            else:
                last_name = player_name_parts[0]
            self.fig.add_annotation(
                x=row["position_x"],  # x-coordinate of the annotation
                y=row["corrected_y"],
                text=str(last_name),  # text to display
                xshift=0,
                yshift=+20,
                showarrow=False,
            )

        # Update the size of the markers
        self.fig.update_traces(marker_size=15)

        # Return the figure and the DataFrames
        return self.fig, df_concat, home_table, away_table
