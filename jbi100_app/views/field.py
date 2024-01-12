from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
from jbi100_app.config import (
    position_mapping_home,
    position_mapping_away,
    player_poss_path,
)

import pandas as pd
import time


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

    def positionPlayer(self, home, away, home_form, away_form, selected_players):
        df_home = self.process_df(home, True)
        df_away = self.process_df(away, False)
        # Bench players also extracted
        df_home_field, df_home_bench = self.select_players(df_home, home_form)
        df_away_field, df_away_bench = self.select_players(df_away, away_form)

        home_table = df_home_bench[["player", "position", "birth_year"]]
        away_table = df_away_bench[["player", "position", "birth_year"]]

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
        # df_concat["selected"] = df_concat["player"].isin(selected_players)
        # Apply conditions directly to create the 'color' column
        df_concat["color"] = df_concat.apply(
            lambda row: "Yellow"
            if row["player"] in selected_players
            else "Blue"
            if row["team"] == home
            else "Red"
            if row["team"] == away
            else "Other",
            axis=1,
        )

        # print(selected_players)
        # print(df_concat.columns)
        # print(df_concat)
        # time.sleep(0.1)
        # player age minutes_90s miscontrols
        # print(px.colors.qualitative.Set1)
        hover_columns = [
            "player",
            # "position",
            # "team",
            "age",
            "minutes_90s",
            "miscontrols"
            # "dispossessed",
            # "passes_received",
            # "progressive_passes_received",
        ]
        color_mapping = {"Green": "green", "Blue": "blue", "Red": "red"}
        self.fig = px.scatter(
            df_concat,
            y="corrected_y",
            x="position_x",
            # color="team",
            color="color",
            symbol="position",
            hover_data=hover_columns,
            height=370,  # Set the height of the figure
            width=900,
            color_discrete_map=color_mapping,
        )
        self.fig.update_layout(
            # margin=dict(l=20, r=20, t=20, b=20),
            margin=dict(l=20, r=20, t=10, b=0),
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor="rgb(0, 200, 0)",
        )
        self.fig.update_xaxes(showticklabels=False)
        self.fig.update_yaxes(showticklabels=False)
        self.fig.update_xaxes(showgrid=True, gridcolor="rgb(0, 128, 0)")
        self.fig.update_yaxes(showgrid=True, gridcolor="rgb(0, 128, 0)")

        # # Update hover template to exclude unwanted columns
        # hover_template = "<br>".join(
        #     [
        #         "{}: %{{customdata[{}]}}".format(col, i)
        #         for i, col in enumerate(hover_columns)
        #     ]
        # )

        # self.fig.update_traces(
        #     hovertemplate=hover_template,
        #     customdata=df_concat[hover_columns].values.tolist(),
        # )

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
                # y=row["position_y"],  # y-coordinate of the annotation
                # name=row["player"],
                # text=str(row["player"]),  # text to display
                text=str(last_name),  # text to display
                xshift=0,
                yshift=+20,
                showarrow=False,
                # showarrow=False,
                # ax=0,
                # ay=-30,
            )

        self.fig.update_traces(marker_size=15)

        return self.fig, df_concat, home_table, away_table
