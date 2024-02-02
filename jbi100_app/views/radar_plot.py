from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random


# csv files used
path_poss = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
path_shoot = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv"
path_pass = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv"

player_names = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]


class Radar(html.Div):
    """
    The Radar class is a subclass of html.Div. It is used to create a radar plot for a list of players.
    The radar plot shows various attributes of the players such as dribbles completed percentage, short passes percentage,
    long passes percentage, medium passes percentage, and shots on target percentage.

    Attributes:
        html_id (str): The id of the HTML div element.
        player_list (list): The list of players for which the radar plot is to be created.
        fig (go.Figure): The figure object of the radar plot.
    """

    def __init__(self, name, list):
        """
        The constructor for Radar class.

        Parameters:
            name (str): The id of the HTML div element.
            list (list): The list of players for which the radar plot is to be created.
        """
        self.html_id = name
        self.player_list = list

        # Equivalent to `html.Div([...])`
        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def plot_radar(self, player_list):
        """
        The function to create the radar plot.

        Parameters:
            player_list (list): The list of players for which the radar plot is to be created.

        Returns:
            go.Figure: The figure object of the radar plot.
        """
        # Read the csv files
        df_poss = pd.read_csv(path_poss)
        df_shoot = pd.read_csv(path_shoot)
        df_pass = pd.read_csv(path_pass)

        # Define the attributes to be plotted
        attributes = [
            ("dribbles_completed_pct", df_poss),
            ("passes_pct_short", df_pass),
            ("passes_pct_long", df_pass),
            ("passes_pct_medium", df_pass),
            ("shots_on_target_pct", df_shoot),
        ]

        # Initialize the list to store the attribute values for each player
        r_extend = []
        for player in player_list:
            player_r = []
            for i, att_info in enumerate(attributes):
                df = att_info[1]
                player_df = df[df["player"] == player]
                # Extract the value of the attribute
                att_val = player_df[att_info[0]].values[0]
                player_r.append(att_val)
            r_extend.append(player_r)

        # Replace nan values with 0
        r_extend = [
            [0 if np.isnan(value) else value for value in inner_list]
            for inner_list in r_extend
        ]

        # Initialize the figure object
        self.fig = go.Figure()

        # Define the categories to be displayed on the plot
        categories = [
            "Dribbles",
            "Short",
            "Long",
            "Medium",
            "Shots",
        ]

        # Define the acceptable colors for the plot
        acceptable_colors = ["green", "purple", "orange", "cyan", "magenta", "brown"]

        # Add a trace for each player
        for i in range(len(player_list)):
            chosen_color = random.choice(acceptable_colors)
            acceptable_colors.remove(chosen_color)

            self.fig.add_trace(
                go.Scatterpolar(
                    r=r_extend[i],
                    theta=categories,
                    line=dict(color=chosen_color),
                    # filling option
                    fill="toself",
                    name=player_list[i],
                )
            )

        # Update the layout of the plot
        self.fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="Passes and Shots on Target(%)",
            height=275,
            width=400,
            margin=dict(t=27, b=0),
        )

        return self.fig
