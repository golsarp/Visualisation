from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px


class Field(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def positionPlayer(self):
        self.fig = px.scatter(
            self.df, y="nation", x="count", color="medal", symbol="medal"
        )
        self.fig.update_traces(marker_size=10)
        # self.fig.show()
        return self.fig
