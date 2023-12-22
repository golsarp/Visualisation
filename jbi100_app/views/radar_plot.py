from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# csv files used
path_poss = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
path_shoot = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv"
path_pass = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv"

player_names = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]


class Radar(html.Div):
    def __init__(self, name, list):
        self.html_id = name
        self.player_list = list

        # Equivalent to `html.Div([...])`
        super().__init__(
            # className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def plot_radar(self, player_list):
        df_poss = pd.read_csv(path_poss)
        df_shoot = pd.read_csv(path_shoot)
        df_pass = pd.read_csv(path_pass)
        attributes = [
            ("dribbles_completed_pct", df_poss),
            ("passes_pct_short", df_pass),
            ("passes_pct_long", df_pass),
            ("passes_pct_medium", df_pass),
            ("shots_on_target_pct", df_shoot),
        ]

        r_extend = []
        for player in player_list:
            player_r = []
            for i, att_info in enumerate(attributes):
                # print(i, att_info[0])
                df = att_info[1]
                player_df = df[df["player"] == player]
                # Extract the value of the 'dribbles_completed_pct' column
                att_val = player_df[att_info[0]].values[0]
                player_r.append(att_val)
            r_extend.append(player_r)

        # make nan values 0
        r_extend = [
            [0 if np.isnan(value) else value for value in inner_list]
            for inner_list in r_extend
        ]
        # features displayed on plot
        self.fig = go.Figure()
        categories = [
            "Dribbles",
            "Short",
            "Long",
            "Medium",
            "Shots",
        ]

        for i in range(len(player_list)):
            self.fig.add_trace(
                go.Scatterpolar(
                    r=r_extend[i],
                    theta=categories,
                    # filling option
                    # fill="toself",
                    name=player_list[i],
                )
            )

        self.fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="Passes and Shots on Target(%)",
            height=300,
            width=400,
            # margin=dict(l=100, r=100, t=100, b=100),
            # legend=dict(x=0, y=1.02),  # Adjust x and y to position the legend on top
        )
        # self.fig.show()

        return self.fig
