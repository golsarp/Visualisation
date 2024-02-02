from dash import dcc, html
import plotly.graph_objects as go


class Scatterplot(html.Div):
    """
    Scatterplot class that extends html.Div. It is used to create and update a scatterplot graph.

    Attributes:
        html_id (str): The id of the html element. It is created by converting the name to lowercase and replacing spaces with hyphens.
        df (DataFrame): The DataFrame that contains the data to be plotted.
        feature_x (str): The name of the column in df that will be plotted on the x-axis.
        feature_y (str): The name of the column in df that will be plotted on the y-axis.
    """

    def __init__(self, name, feature_x, feature_y, df):
        """
        The constructor for Scatterplot class.

        Parameters:
            name (str): The name of the scatterplot.
            feature_x (str): The name of the column in df that will be plotted on the x-axis.
            feature_y (str): The name of the column in df that will be plotted on the y-axis.
            df (DataFrame): The DataFrame that contains the data to be plotted.
        """
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        super().__init__(
            className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def update(self, selected_color, selected_data):
        """
        The function to update the scatterplot with new data and color.

        Parameters:
            selected_color (str): The color to be used for the selected points.
            selected_data (dict): The data to be plotted. If it is None, all points in df are plotted.

        Returns:
            fig: The updated figure.
        """
        self.fig = go.Figure()

        x_values = self.df[self.feature_x]
        y_values = self.df[self.feature_y]
        self.fig.add_trace(
            go.Scatter(
                x=x_values, y=y_values, mode="markers", marker_color="rgb(200,200,200)"
            )
        )
        self.fig.update_traces(mode="markers", marker_size=10)
        self.fig.update_layout(
            yaxis_zeroline=False, xaxis_zeroline=False, dragmode="select"
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        # highlight points with selection other graph
        if selected_data is None:
            selected_index = self.df.index  # show all
        else:
            selected_index = [  # show only selected indices
                x.get("pointIndex", None) for x in selected_data["points"]
            ]

        self.fig.data[0].update(
            selectedpoints=selected_index,
            # color of selected points
            selected=dict(marker=dict(color=selected_color)),
            # color of unselected pts
            unselected=dict(marker=dict(color="rgb(200,200,200)", opacity=0.9)),
        )

        # update axis titles
        self.fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
        )

        return self.fig
