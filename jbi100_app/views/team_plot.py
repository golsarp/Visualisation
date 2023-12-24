from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os



class Bar(html.Div):
    def __init__(self, name, feature_list, teams_list, feature_values):
        self.html_id = name
        self.features = feature_list
        self.teams = teams_list
        self.feature_values = feature_values

        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def plot_bar(self, features, teams, feature_values):

        # get player values
        # TODO: either calculate player values here or pass them as parameter

        fig = go.Figure()

        for team, f_value in zip(teams, feature_values):
            fig.add_trace(go.Bar(name=team, x=features, y=f_value))

        fig.update_layout(barmode='group')
        fig.show()


# Usage:
categories = ['penalties', 'shots on goal', 'fouls']
compared_teams = ['Germany', 'Netherlands']
player_values = [[20, 14, 23], [12, 18, 29]]  # Germany (all three categories), Netherlands (all three categories)


# get current wd
current_wd = os.getcwd()

# go to top level wd
current_wd = current_wd.replace('/jbi100_app/views', '')

# path to csv files
path_poss = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv'
path_shoot = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv'
path_pass = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv'

# player_names = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]

df_poss = pd.read_csv(path_poss)
df_shoot = pd.read_csv(path_shoot)
df_pass = pd.read_csv(path_pass)

# print(df_poss)
# print(df_shoot)
# print(df_pass)
# print(player_names)

# TODO: either pass player names as parameter and calculate parameters in plot_bar or calculate parameters here,
#  and pass them as parameter
Bar.plot_bar("plot", categories, compared_teams, player_values)




