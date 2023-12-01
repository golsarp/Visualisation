from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
)

import pandas as pd


class Field(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            # className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def process_df(self, team, home):
        df = pd.read_csv(player_poss_path)
        df_team = df[df["team"] == team].copy()
        df_team = df_team.sort_values(by="position")
        mapping = position_mapping_home if home else position_mapping_away

        df_team["position_x"] = df_team["position"].map(mapping)
        df_team["position_y"] = df_team.groupby("position").cumcount() + 1

        return df_team

    def positionPlayer(self, home, away):
        df_home = self.process_df(home, True)
        df_away = self.process_df(away, False)
        df_concat = pd.concat([df_home, df_away], ignore_index=True)
        self.fig = px.scatter(
            df_concat,
            y="position_y",
            x="position_x",
            color="position",
            symbol="position",
        )
        # fig = px.scatter(self.df, y="nation", x="count", color="medal", symbol="medal")
        # Add annotations (text on top of values)
        for i, row in df_concat.iterrows():
            self.fig.add_annotation(
                x=row["position_x"],  # x-coordinate of the annotation
                y=row["position_y"],  # y-coordinate of the annotation
                # name=row["player"],
                text=str(row["player"]),  # text to display
                # showarrow=True,
                # arrowhead=2,
                # arrowcolor="black",
                # arrowsize=1,
                # arrowwidth=2,
                ax=0,
                ay=-40,
            )
        self.fig.update_traces(marker_size=10)
        # self.fig.show()
        return self.fig
