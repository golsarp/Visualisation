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

        group["corrected_y"] = group["position_y"] * factor

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

    # 0 home color , 1 away color , 2 field color, 3 home bench color,  4 away bench color , 5 selected bench color,

        df_concat["color"] = df_concat.apply(
            lambda row: colors[7]
            if row["player"] == away_field_pl
            else colors[7]
            if row["player"] == home_field_pl
            else colors[5]
            if row["player"] in selected_players
            else colors[14]
            if row["player"] in bar_players
            else colors[0]
            if row["team"] == home
            else colors[1]
            if row["team"] == away
            else "Other",
            axis=1,
        )

        hover_columns = [
            "player",
            "age",
            "minutes_90s",
            "miscontrols"
        ]
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

        color_list = [colors[0], colors[1], colors[5], colors[3], colors[4], colors[7], colors[14]]

        for color_value in color_list:
            self.fig.for_each_trace(
                lambda trace: trace.update(hovertemplate=trace.hovertemplate.replace(f'color={color_value}<br>', ''))
            )

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

        self.fig.update_traces(marker_size=15)

        return self.fig, df_concat, home_table, away_table
