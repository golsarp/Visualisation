from dash import dcc, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


class Table(html.Div):
    def __init__(self, name):
        self.html_id = name

        # Equivalent to `html.Div([...])`
        super().__init__(
            # className="graph_card",
            # children=[html.H6(name), dcc.Graph(id=self.html_id)],
            children=[
                dash_table.DataTable(
                    id=self.html_id,
                )
            ],
        )

    def plot_table(self, df,home,colors):
        # print(df.columns)
        # df["birth_year"] = 2023 - df["birth_year"]
        # new_col_names = {
        #      "Player",
        #     "position": "Position",
        #     "birth_year": "Age",
        # }
        #print("colors ",colors)
        use = None
        if home:
            use = colors[3]
        else:
            use = colors[4]
            

        # df = df.rename(columns=new_col_names)
        selected_columns = ["player", "position", "age"]
        df = df[selected_columns]
        # print(df)
        return (
            dash_table.DataTable(
                id=self.html_id,
                columns=[{"name": i, "id": i} for i in df.columns],
                # columns=new_columns,
                data=df.to_dict("records"),
                style_cell=dict(textAlign="left"),
                style_header=dict(backgroundColor=colors[9]),
                style_data=dict(backgroundColor=use),
                style_data_conditional=[
                    {
                        "if": {"column_id": col, "column_editable": False},
                        "backgroundColor": colors[8],
                        "pointer-events": "none",  # Disable clicking on non-"player" columns
                    }
                    for col in df.columns
                    if col != "player"
                ]
                + [
                    {
                        "if": {"column_id": "player", "state": "active"},
                        "backgroundColor": colors[7],
                    }
                ],
                virtualization=True,  # Enable virtualization for infinite scrolling
                fixed_rows={"headers": True},  # Keep header fixed at the top
                style_table={
                    "height": "250px",
                    # "width": "400px",
                    "overflowY": "auto",
                },  #
            ),
        )
