from dash import Dash, html, Input, Output, dash_table, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash

position_mapping_home = {"GK": 1, "DF": 2, "MF": 4, "FW": 6}

position_mapping_away = {"GK": 13, "DF": 12, "MF": 10, "FW": 8}

player_poss_path = (
    "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
)


def process_df(team, home):
    df = pd.read_csv(player_poss_path)
    df_team = df[df["team"] == team].copy()
    df_team = df_team.sort_values(by="position")
    mapping = position_mapping_home if home else position_mapping_away

    df_team["position_x"] = df_team["position"].map(mapping)
    df_team["position_y"] = df_team.groupby("position").cumcount() + 1

    return df_team


def select_players(df, formation):
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


home = "Australia"
away = "Qatar"
home_form = "5-3-2-1"
away_form = "4-2-3-1"
df_home = process_df(home, True)
df_away = process_df(away, False)
# Bench players also extracted
df_home_field, df_home_bench = select_players(df_home, home_form)
df_away_field, df_away_bench = select_players(df_away, away_form)
# print(df_home)
df_home_bench_subset = df_home_bench[["player", "position", "birth_year"]]
df_away_bench_subset = df_away_bench[["player", "position", "birth_year"]]
print(df_home_bench_subset)


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Your Dash App"),
        # First DataTable
        html.Div(
            [
                html.H2("Home Bench"),
                html.P(id="table_out_home"),
                dash_table.DataTable(
                    id="table_home",
                    columns=[
                        {"name": i, "id": i} for i in df_home_bench_subset.columns
                    ],
                    data=df_home_bench_subset.to_dict("records"),
                    style_cell=dict(textAlign="left"),
                    style_header=dict(backgroundColor="paleturquoise"),
                    style_data=dict(backgroundColor="lavender"),
                    style_data_conditional=[
                        {
                            "if": {"column_id": col, "column_editable": False},
                            "backgroundColor": "rgba(255, 0, 0, 0.1)",
                            "pointer-events": "none",  # Disable clicking on non-"player" columns
                        }
                        for col in df_home_bench_subset.columns
                        if col != "player"
                    ]
                    + [
                        {
                            "if": {"column_id": "player", "state": "active"},
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        }
                    ],
                ),
            ],
            style={"display": "inline-block", "width": "48%"},  # Adjust width as needed
        ),
        html.Div(
            [
                html.H2("Away Bench"),
                html.P(id="table_out_away"),
                dash_table.DataTable(
                    id="table_away",
                    columns=[
                        {"name": i, "id": i} for i in df_away_bench_subset.columns
                    ],
                    data=df_away_bench_subset.to_dict("records"),
                    style_cell=dict(textAlign="left"),
                    style_header=dict(backgroundColor="paleturquoise"),
                    style_data=dict(backgroundColor="lavender"),
                    style_data_conditional=[
                        {
                            "if": {"column_id": col, "column_editable": False},
                            "backgroundColor": "rgba(255, 0, 0, 0.1)",
                            "pointer-events": "none",  # Disable clicking on non-"player" columns
                        }
                        for col in df_away_bench_subset.columns
                        if col != "player"
                    ]
                    + [
                        {
                            "if": {"column_id": "player", "state": "active"},
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        }
                    ],
                ),
            ],
            style={"display": "inline-block", "width": "48%"},  # Adjust width as needed
        ),
    ]
)


@app.callback(Output("table_out_home", "children"), Input("table_home", "active_cell"))
def update_graph_home(active_cell):
    if active_cell:
        cell_data = df_home_bench_subset.iloc[active_cell["row"]][
            active_cell["column_id"]
        ]
        return f'Data: "{cell_data}" from table cell: {active_cell}'
    return "Click the Players to Swap"


@app.callback(Output("table_out_away", "children"), Input("table_away", "active_cell"))
def update_graph_away(active_cell):
    if active_cell:
        cell_data = df_away_bench_subset.iloc[active_cell["row"]][
            active_cell["column_id"]
        ]
        return f'Data: "{cell_data}" from table cell: {active_cell}'
    return "Click the table"


# @app.callback(Output("table_out_away", "children"), Input("table_away", "active_cell"))
# def update_graphs(active_cell):
#     if active_cell:
#         if active_cell["column_id"] == "player":
#             cell_data = df_away_bench_subset.iloc[active_cell["row"]][
#                 active_cell["column_id"]
#             ]
#             return f'Data: "{cell_data}" from table cell: {active_cell}'
#     return "Click the table"


app.run_server(debug=True)
