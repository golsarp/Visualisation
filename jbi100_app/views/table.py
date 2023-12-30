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
            children=[dcc.Graph(id=self.html_id)],
        )

    def plot_table(self, df):
        table = (
            dash_table.DataTable(
                id=self.html_id,
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_cell=dict(textAlign="left"),
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_data_conditional=[
                    {
                        "if": {"column_id": col, "column_editable": False},
                        "backgroundColor": "rgba(255, 0, 0, 0.1)",
                        "pointer-events": "none",  # Disable clicking on non-"player" columns
                    }
                    for col in df.columns
                    if col != "player"
                ]
                + [
                    {
                        "if": {"column_id": "player", "state": "active"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    }
                ],
            ),
        )
        return table
