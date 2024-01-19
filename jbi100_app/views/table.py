from dash import html, dash_table


class Table(html.Div):
    def __init__(self, name):
        self.html_id = name

        super().__init__(
            children=[
                dash_table.DataTable(
                    id=self.html_id,
                )
            ],
        )

    def plot_table(self, df, home, colors):

        if home:
            use = colors[3]
        else:
            use = colors[4]

        selected_columns = ["player", "position", "age"]
        df = df[selected_columns]

        return (
            dash_table.DataTable(
                id=self.html_id,
                columns=[{"name": i, "id": i} for i in df.columns],
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
                    "overflowY": "auto",
                },
            ),
        )
