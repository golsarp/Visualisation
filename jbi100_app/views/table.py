from dash import html, dash_table


class Table(html.Div):
    """
    Table class used for the home and away bench.

    ...

    Attributes
    ----------
    html_id : str
        a formatted string to set the id of the DataTable

    Methods
    -------
    plot_table(df, home, colors)
        Plots the table with the given dataframe, home flag and colors.
    """

    def __init__(self, name):
        """
        Constructs all the necessary attributes for the Table object.

        Parameters
        ----------
            name : str
                the id of the DataTable
        """
        self.html_id = name

        super().__init__(
            children=[
                dash_table.DataTable(
                    id=self.html_id,
                )
            ],
        )

    def plot_table(self, df, home, colors):
        """
        Plots the table with the given dataframe, home flag and colors.

        Parameters
        ----------
            df : DataFrame
                the dataframe to be plotted
            home : bool
                flag to determine the color of the table
            colors : list
                list of colors to be used in the table

        Returns
        -------
        DataTable
            the plotted DataTable
        """
        if home:
            use = colors[3]
        else:
            use = colors[4]

        selected_columns = ["player", "position", "age"]
        df = df[selected_columns]

        return (
            dash_table.DataTable(
                # The id of the DataTable
                id=self.html_id,
                # The columns of the DataTable
                columns=[{"name": i, "id": i} for i in df.columns],
                # The data of the DataTable
                data=df.to_dict("records"),
                # The style of the cells
                style_cell=dict(textAlign="left"),
                # The style of the header
                style_header=dict(backgroundColor=colors[9]),
                # The style of the data
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
                        "backgroundColor": colors[7], # The style of the active player
                    }
                ],
                virtualization=True,  # Enable virtualization for infinite scrolling
                fixed_rows={"headers": True},  # Keep header fixed at the top
                style_table={
                    "height": "250px",
                    "overflowY": "auto",  # The style of the table
                },
            ),
        )
