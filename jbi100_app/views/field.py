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
    def __init__(self, name, feature_x, feature_y):
        self.html_id = name.lower().replace(" ", "-")

        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            # className="graph_card",
            # children=[html.H6(name), dcc.Graph(id=self.html_id)],
            children=[dcc.Graph(id=self.html_id)],
        )

    def select_players(self, df, formation):
        positions = formation.split("-")
        positions = list(map(int, positions))
        selected_players = pd.DataFrame()
        bench_players = pd.DataFrame()

        i = 0
        for pos in positions:
            position_df = df[
                df["position"].str.startswith(
                    "FW" if i == 0 else "MF" if i == 1 else "DF" if i == 2 else "GK"
                )
            ]
            selected_players = pd.concat([selected_players, position_df.head(pos)])
            bench_players = pd.concat([bench_players, position_df.tail(-pos)])

            i += 1

        return selected_players, bench_players

    def process_df(self, team, home):
        df = pd.read_csv(player_poss_path)
        df_team = df[df["team"] == team].copy()
        df_team = df_team.sort_values(by="position")
        mapping = position_mapping_home if home else position_mapping_away

        df_team["position_x"] = df_team["position"].map(mapping)
        df_team["position_y"] = df_team.groupby("position").cumcount() + 1

        return df_team

    def calculate_corrected_y(self, group, max_val):
        # You can customize the factor as needed
        factor = max_val / (len(group) + 1)
        # print("factor ", factor)
        # print("group ", group)
        # group["numeric_y"] = pd.to_numeric(group["position_y"], errors="coerce")
        res = group["position_y"] * factor
        # print("res is ", res)
        # print("gorup after ")
        # group["res"] = group["position_y"] * factor

        group["corrected_y"] = group["position_y"] * factor
        # print("gorup after ")
        # print(group)

        return group["corrected_y"]

    def positionPlayer(self, home, away, home_form, away_form):
        df_home = self.process_df(home, True)
        df_away = self.process_df(away, False)
        # Bench players also extracted
        df_home_field, df_home_bench = self.select_players(df_home, home_form)
        df_away_field, df_away_bench = self.select_players(df_away, away_form)

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

        hover_columns = [
            "player",
            # "position",
            # "team",
            "age",
            "birth_year",
            # "dispossessed",
            # "passes_received",
            # "progressive_passes_received",
        ]

        self.fig = px.scatter(
            df_concat,
            y="corrected_y",
            # y="position_y",
            x="position_x",
            color="position",
            symbol="position",
            hover_data=hover_columns,
            height=400,  # Set the height of the figure
            width=900,
        )

        # Add annotations (text on top of values)
        for i, row in df_concat.iterrows():
            self.fig.add_annotation(
                x=row["position_x"],  # x-coordinate of the annotation
                y=row["corrected_y"],
                # y=row["position_y"],  # y-coordinate of the annotation
                # name=row["player"],
                text=str(row["player"]),  # text to display
                ax=0,
                ay=-40,
            )

        self.fig.update_traces(marker_size=10)

        return self.fig
