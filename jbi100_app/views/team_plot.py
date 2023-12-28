import numpy as np
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
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

    def plot_bar(self, categories, teams, names):

        df_poss, df_shoot, df_pass = get_datasets()

        nr_features = len(categories)

        team_zero_values = [0] * nr_features
        team_one_values = [0] * nr_features

        attributes = {
            "dribbles_completed_pct": df_poss,
            "passes_pct_short": df_pass,
            "passes_pct_long": df_pass,
            "passes_pct_medium": df_pass,
            "shots_on_target_pct": df_shoot,
        }

        for player in names:

            player_team = df_poss[df_poss["player"] == player]["team"].values[0]

            for feature in categories:

                feature_df = attributes[feature]

                player_row = feature_df.loc[feature_df['player'] == player]

                player_value = player_row[feature].values[0]

                if np.isnan(player_value):
                    player_value = 0

                if player_team in teams[0]:

                    temp_zero_value = team_zero_values[categories.index(feature)]

                    new_zero_value = temp_zero_value + player_value

                    team_zero_values[categories.index(feature)] = new_zero_value

                elif player_team in teams[1]:

                    temp_one_value = team_one_values[categories.index(feature)]

                    new_one_value = temp_one_value + player_value

                    team_one_values[categories.index(feature)] = new_one_value

                # else:
                #     raise ValueError(f'{player} is not a player in one of the selected teams')

        feature_values = [team_zero_values, team_one_values]

        self.fig = go.Figure()

        for team, f_value in zip(teams, feature_values):
            self.fig.add_trace(go.Bar(name=team, x=categories, y=f_value))

        self.fig.update_layout(barmode='group')
        # fig.show()
        return self.fig


def get_datasets():
    # get current wd
    current_wd = os.getcwd()
    # go to top level wd
    current_wd = current_wd.replace('/jbi100_app/views', '')
    # path to csv files
    path_poss = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv'
    path_shoot = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv'
    path_pass = f'{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv'
    # path to df
    df_poss = pd.read_csv(path_poss)
    df_shoot = pd.read_csv(path_shoot)
    df_pass = pd.read_csv(path_pass)

    return df_poss, df_shoot, df_pass


if __name__ == "__main__":
    # Usage:
    features = ["dribbles_completed_pct", "passes_pct_short", "shots_on_target_pct"]
    compared_teams = ['Portugal', 'Wales']
    player_names = ["Cristiano Ronaldo", "Aaron Ramsey", "André Silva"]

    Bar.plot_bar("plot", features, compared_teams, player_names)
