import numpy as np
from dash import dcc, html
import pandas as pd
import os
import plotly.express as px


class Bar(html.Div):
    """
    A class used to represent a Bar plot.

    Attributes
    ----------
    fig : plotly.graph_objs._figure.Figure
        a plotly figure object that represents the bar plot
    html_id : str
        a string that represents the id of the html element
    features : list
        a list of features to be plotted
    teams : list
        a list of teams to be plotted
    feature_values : list
        a list of feature values to be plotted
    sorted_plot_df : pandas.DataFrame
        a pandas DataFrame that contains the sorted plot data

    Methods
    -------
    plot_bar(categories, names, color_list, home_team, away_team, percent_df=None)
        Plots the bar chart based on the provided parameters.
    get_dataframe()
        Returns the sorted plot DataFrame.
    """
    def __init__(self, name, feature_list, teams_list, feature_values):
        """
        Constructs all the necessary attributes for the Bar object.

        Parameters
        ----------
            name : str
                the name of the Bar object
            feature_list : list
                the list of features to be plotted
            teams_list : list
                the list of teams to be plotted
            feature_values : list
                the list of feature values to be plotted
        """
        self.fig = None
        self.html_id = name
        self.features = feature_list
        self.teams = teams_list
        self.feature_values = feature_values
        self.sorted_plot_df = None

        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def plot_bar(self, categories, names, color_list, home_team, away_team, percent_df=None):
        """
        Plots the bar chart based on the provided parameters.

        Parameters
        ----------
            categories : list
                the list of categories to be plotted
            names : list
                the list of names to be plotted
            color_list : list
                the list of colors to be used in the plot
            home_team : str
                the name of the home team
            away_team : str
                the name of the away team
            percent_df : pandas.DataFrame, optional
                a pandas DataFrame that contains the percentage data (default is None)

        Returns
        -------
            plotly.graph_objs._figure.Figure
                a plotly figure object that represents the bar plot
        """
        column_name_to_alias = {
            "dribbles_completed": "Dribbles",
            "passes_short": "Short",
            "passes_medium": "Medium",
            "passes_long": "Long",
            "shots_on_target": "Shots",
            "goals": "Goals",
        }

        color_mapping = {
            color_list[0]: color_list[0],
            color_list[1]: color_list[1]
        }

        if percent_df is None:

            df_poss, df_shoot, df_pass = get_datasets()

            attributes = {
                "dribbles_completed": df_poss,
                "passes_short": df_pass,
                "passes_long": df_pass,
                "passes_medium": df_pass,
                "shots_on_target": df_shoot,
                "goals": df_shoot,
            }

            plot_df = pd.DataFrame(columns=["name", "team", "feature", "value"])

            for player in names:
                player_team = df_poss[df_poss["player"] == player]["team"].values[0]

                for feature in categories:
                    feature_df = attributes[feature]

                    player_row = feature_df.loc[feature_df["player"] == player]

                    player_value = player_row[feature].values[0]

                    if np.isnan(player_value):
                        player_value = 0

                    new_row = {
                        "name": player,
                        "team": player_team,
                        "feature": feature,
                        "value": player_value,
                    }

                    plot_df = pd.concat(
                        [plot_df, pd.DataFrame(new_row, index=[0])], ignore_index=True
                    )

            sorted_plot_df = plot_df.sort_values(
                ["team", "feature", "value"], ascending=[True, True, False]
            )

            # Replace the feature names with their aliases in the dataframe
            sorted_plot_df['feature'] = sorted_plot_df['feature'].map(column_name_to_alias)

            sorted_plot_df['color'] = np.where(sorted_plot_df['team'] == home_team, color_list[0], color_list[1])

            self.fig = px.bar(
                sorted_plot_df,
                x="feature",
                y="value",
                color="color",
                barmode="group",
                hover_name="name",
                hover_data={"team": False, "feature": False, "value": True, "color": False},
                title="Team passes & Shots",
                custom_data=['name'],
                color_discrete_map=color_mapping,
                height=400
            )

            self.fig.update_layout(
                legend={"title": "Teams"},
                xaxis_title=None,
                yaxis_title="Occurrences",
                margin=dict(l=20, r=20, t=40, b=0),
                clickmode="event",
            )

        else:
            sorted_plot_df = percent_df

            sorted_plot_df['color'] = np.where(sorted_plot_df['team'] == home_team, color_list[0], color_list[1])

            self.fig = px.bar(
                sorted_plot_df,
                x="feature",
                y="value",
                color="color",
                barmode="group",
                hover_name="name",
                hover_data={"team": False, "feature": False, "value": True, "color": False},
                title="Team passes & Shots",
                custom_data=['name'],
                color_discrete_map=color_mapping,
                height=400
            )

            self.fig.update_layout(
                legend={"title": "Teams"},
                xaxis_title=None,
                yaxis_title="Percentage",
                margin=dict(l=20, r=20, t=40, b=20),
                clickmode="event",
            )

        # Customize legend labels for specific colors
        legend_labels = {'rgb(255,0,0)': home_team, 'rgb(0,255,0)': away_team}
        for trace, legend_label in zip(self.fig.data, legend_labels.values()):
            trace.name = legend_label

        self.sorted_plot_df = sorted_plot_df

        return self.fig

    def get_dataframe(self):
        """
        Returns the sorted plot DataFrame.

        Returns
        -------
            pandas.DataFrame
                a pandas DataFrame that contains the sorted plot data
        """
        return self.sorted_plot_df


def get_datasets():
    """
    Returns the datasets required for the plot.

    Returns
    -------
        tuple
            a tuple containing three pandas DataFrames that represent the possession, shooting, and passing data
    """
    # get current wd
    current_wd = os.getcwd()
    # go to top level wd
    current_wd = current_wd.replace("/jbi100_app/views", "")
    # path to csv files
    path_poss = f"{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
    path_shoot = f"{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv"
    path_pass = f"{current_wd}/FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv"
    # path to df
    df_poss = pd.read_csv(path_poss)
    df_shoot = pd.read_csv(path_shoot)
    df_pass = pd.read_csv(path_pass)

    return df_poss, df_shoot, df_pass
