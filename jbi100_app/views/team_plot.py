import numpy as np
from dash import dcc, html
import pandas as pd
import os
import plotly.express as px


class Bar(html.Div):
    def __init__(self, name, feature_list, teams_list, feature_values):
        self.fig = None
        self.html_id = name
        self.features = feature_list
        self.teams = teams_list
        self.feature_values = feature_values

        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def plot_bar(self, categories, names):

        df_poss, df_shoot, df_pass = get_datasets()

        attributes = {
            "dribbles_completed": df_poss,
            "passes_short": df_pass,
            "passes_long": df_pass,
            "passes_medium": df_pass,
            "shots_on_target": df_shoot,
        }

        plot_df = pd.DataFrame(columns=['name', 'team', 'feature', 'value'])

        for player in names:

            player_team = df_poss[df_poss["player"] == player]["team"].values[0]

            for feature in categories:

                feature_df = attributes[feature]

                player_row = feature_df.loc[feature_df['player'] == player]

                player_value = player_row[feature].values[0]

                if np.isnan(player_value):
                    player_value = 0

                new_row = {'name': player, 'team': player_team, 'feature': feature, 'value': player_value}

                plot_df = pd.concat([plot_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

        sorted_plot_df = plot_df.sort_values(['feature', 'value'], ascending=[True, False])

        self.fig = px.bar(sorted_plot_df, x='feature', y='value', color='team', barmode='group',
                          hover_name='name', hover_data={'team': False, 'feature': False, 'value': True}
                          , title='Team plot')

        self.fig.update_layout(legend={"title": "Teams"}, xaxis_title=None, yaxis_title='Nr of times')

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
