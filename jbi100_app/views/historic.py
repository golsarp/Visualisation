import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd

# csv files used
file_path = "FIFA DataSet/Data/FIFA World Cup Historic/matches_1930_2022.csv"




# app.layout = html.Div([
#     html.Label('Select Home Team'),
#     dcc.Dropdown(
#         id='home-team-dropdown',
#         options=team_options,
#         value=teams[0]
#     ),
#     html.Label('Select Away Team'),
#     dcc.Dropdown(
#         id='away-team-dropdown',
#         options=team_options,
#         value=teams[1]
#     ),
#     dcc.Graph(id='graph')
# ])

# @app.callback(
#     dash.dependencies.Output('graph', 'figure'),
#     [
#         dash.dependencies.Input('home-team-dropdown', 'value'),
#         dash.dependencies.Input('away-team-dropdown', 'value')
#     ]
# )

class Historic(html.Div):
    def __init__(self, name):
        self.html_id = name
        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def build_historic(self, home_team, away_team):
        df = pd.read_csv(file_path)

        # Get unique team names
        teams = pd.concat([df['home_team'], df['away_team']]).unique()
        team_options = [{'label': team, 'value': team} for team in teams]
        filtered_home_df = df[df['home_team'] == home_team].copy()
        filtered_away_df = df[df['away_team'] == away_team].copy()

        # Create a new figure
        self.figure = go.Figure()

        # Add a bar for the home team
        # Add a line for the home team
        self.figure.add_trace(go.Scatter(
            x=filtered_home_df['Date'],  # Replace 'Year' with the appropriate column from your DataFrame
            y=filtered_home_df['home_score'],  # Replace 'home_score' with the appropriate column from your DataFrame
            mode='lines+markers',
            name=home_team
        ))

        # Add a line for the away team
        self.figure.add_trace(go.Scatter(
            x=filtered_away_df['Date'],  # Replace 'Year' with the appropriate column from your DataFrame
            y=filtered_away_df['away_score'],  # Replace 'away_score' with the appropriate column from your DataFrame
            mode='lines+markers',
            name=away_team
        ))
        # Add range slider
        self.figure.update_layout(
            title='Historic Match Scores',
            width=400,
            height=400,
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        return self.figure
