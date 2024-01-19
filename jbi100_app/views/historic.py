from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd

# csv files used
file_path = "FIFA DataSet/Data/FIFA World Cup Historic/matches_1930_2022.csv"


class Historic(html.Div):
    def __init__(self, name):
        self.html_id = name
        super().__init__(
            children=[dcc.Graph(id=self.html_id)],
        )

    def build_historic(self, team1, team2, colors):
        df = pd.read_csv(file_path)
        df["Year"] = df["Year"].astype(int)
        # Create an empty figure
        self.figure = go.Figure()

        # Team 1 home scores
        home_scores_by_year_team1 = df[df["home_team"] == team1][
            ["Year", "home_score", "away_score", "away_team", "home_team"]
        ]
        home_scores_by_year_team1["is_winner"] = (
            home_scores_by_year_team1["home_score"]
            > home_scores_by_year_team1["away_score"]
        )
        home_scores_by_year_team1 = home_scores_by_year_team1.drop(
            columns=["away_score"]
        )

        # Team 2 home scores
        home_scores_by_year_team2 = df[df["home_team"] == team2][
            ["Year", "home_score", "away_score", "away_team", "home_team"]
        ]
        home_scores_by_year_team2["is_winner"] = (
            home_scores_by_year_team2["home_score"]
            > home_scores_by_year_team2["away_score"]
        )
        home_scores_by_year_team2 = home_scores_by_year_team2.drop(
            columns=["away_score"]
        )

        # Team 1 away scores
        away_scores_by_year_team1 = df[df["away_team"] == team1][
            ["Year", "away_score", "home_score", "home_team", "away_team"]
        ]
        away_scores_by_year_team1["is_winner"] = (
            away_scores_by_year_team1["away_score"]
            > away_scores_by_year_team1["home_score"]
        )
        away_scores_by_year_team1 = away_scores_by_year_team1.drop(
            columns=["home_score"]
        )

        # Team 2 away scores
        away_scores_by_year_team2 = df[df["away_team"] == team2][
            ["Year", "away_score", "home_score", "home_team", "away_team"]
        ]
        away_scores_by_year_team2["is_winner"] = (
            away_scores_by_year_team2["away_score"]
            > away_scores_by_year_team2["home_score"]
        )
        away_scores_by_year_team2 = away_scores_by_year_team2.drop(
            columns=["home_score"]
        )

        # Concatenate home and away scores for each team
        scores_by_year_team1 = pd.concat(
            [home_scores_by_year_team1, away_scores_by_year_team1]
        )
        scores_by_year_team1 = scores_by_year_team1.sort_values("Year")

        scores_by_year_team2 = pd.concat(
            [home_scores_by_year_team2, away_scores_by_year_team2]
        )
        scores_by_year_team2 = scores_by_year_team2.sort_values("Year")

        unique_years = list(
            set(scores_by_year_team1["Year"]).union(set(scores_by_year_team2["Year"]))
        )
        unique_years.sort()

        # Define a custom color scale function
        def get_color(is_home_team, is_home, is_winner):
            
            # Define the base color for home and away
            if is_home_team:
                base_color_home = colors[11]     # Red  10,11,12,13
                base_color_away = colors[12]       # green    
            else:
                base_color_home = colors[10]     # blue # orange 
                base_color_away = colors[13]
            color = base_color_home if is_home else base_color_away
            if is_winner:
                adjusted_color = "rgba({}, {}, {}, {})".format(
                    int(color[0]), int(color[1]), int(color[2]), 1
                )
            else:
                adjusted_color = "rgba({}, {}, {}, {})".format(
                    int(color[0]), int(color[1]), int(color[2]), 0.5
                )
            return adjusted_color

        # Initialize a dictionary to track whether the legend item has been added
        legend_added_team1 = {"Home Score": False, "Away Score": False}
        legend_added_team2 = {"Home Score": False, "Away Score": False}

        # Add traces for home scores team 1
        for index, row in home_scores_by_year_team1.iterrows():
            show_legend = False
            if not legend_added_team1["Home Score"]:
                show_legend = True
                legend_added_team1["Home Score"] = True

            if pd.isna(row["home_score"]) or row["home_team"] != team1:
                continue

            self.figure.add_trace(
                go.Bar(
                    x=[f"{row['home_team']} ({row['Year']})"],
                    y=[row["home_score"]],
                    name="Home Scores For " + str(row["home_team"]),
                    marker_color=get_color(True, True, row["is_winner"]),
                    hoverinfo="y+text",
                    hovertext="Won Against " + str(row["away_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["away_team"]),
                    showlegend=show_legend,
                    legendgroup="Home Scores Team 1",
                )
            )

        # Add traces for away scores team 1
        for index, row in away_scores_by_year_team1.iterrows():
            show_legend = False
            if not legend_added_team1["Away Score"]:
                show_legend = True
                legend_added_team1["Away Score"] = True

            if pd.isna(row["away_score"]) or row["away_team"] != team1:
                continue

            self.figure.add_trace(
                go.Bar(
                    x=[f"{row['away_team']} ({row['Year']})"],
                    y=[row["away_score"]],
                    name="Away Scores For " + str(row["away_team"]),
                    marker_color=get_color(True, False, row["is_winner"]),
                    hoverinfo="y+text",
                    hovertext="Won Against " + str(row["home_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["home_team"]),
                    showlegend=show_legend,
                    legendgroup="Away Scores Team 1",
                )
            )

        # Add traces for home scores team 2
        for index, row in home_scores_by_year_team2.iterrows():
            show_legend = False
            if not legend_added_team2["Home Score"]:
                show_legend = True
                legend_added_team2["Home Score"] = True

            if pd.isna(row["home_score"]) or row["home_team"] != team2:
                continue

            self.figure.add_trace(
                go.Bar(
                    x=[f"{row['home_team']} ({row['Year']})"],
                    y=[row["home_score"]],
                    name="Home Scores For " + str(row["home_team"]),
                    marker_color=get_color(False, True, row["is_winner"]),
                    hoverinfo="y+text",
                    hovertext="Won Against " + str(row["away_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["away_team"]),
                    showlegend=show_legend,
                    legendgroup="Home Scores Team 2",
                )
            )

        # Add traces for away scores team 2
        for index, row in away_scores_by_year_team2.iterrows():
            show_legend = False
            if not legend_added_team2["Away Score"]:
                show_legend = True
                legend_added_team2["Away Score"] = True

            if pd.isna(row["away_score"]) or row["away_team"] != team2:
                continue

            self.figure.add_trace(
                go.Bar(
                    x=[f"{row['away_team']} ({row['Year']})"],
                    y=[row["away_score"]],
                    name="Away Scores For " + str(row["away_team"]),
                    marker_color=get_color(False, False, row["is_winner"]),
                    hoverinfo="y+text",
                    hovertext="Won Against " + str(row["home_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["home_team"]),
                    showlegend=show_legend,
                    legendgroup="Away Scores Team 2",
                )
            )
        ordered_categories = []
        tickvals = []
        ticktext = []
        for i, year in enumerate(unique_years):
            ordered_categories.append(f"{team1} ({year})")
            ordered_categories.append(f"{team2} ({year})")
            tickvals.append(i * 2 + 0.5)
            ticktext.append(str(year))

        # A dictionary for each x-axis
        xaxes = {
            "xaxis": dict(
                domain=[0, 1],
                anchor="y",
                showticklabels=True,
                fixedrange=True,
                tickmode="array",
                tickvals=tickvals,
                ticktext=ticktext,
                categoryorder="array",
                categoryarray=ordered_categories,
            )
        }

        # Annotation for the x-axis title
        annotations = [
            dict(
                x=0.5,
                y=-0.1,
                text="",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=15),
                xanchor="center",
                yanchor="top",
            )
        ]

        # Custom layout
        self.figure.update_layout(
            barmode="stack",
            title=f"{team1} and {team2} Historical Scores by Year",
            yaxis_title="Score",
            yaxis=dict(fixedrange=True),
            annotations=annotations,
            margin=dict(l=50, r=50, t=50, b=50),
            legend=dict(
                y=1,
                yanchor="auto",
                x=1,
                xanchor="auto",
                bgcolor="rgba(0,0,0,0)",
                font=dict(size=10),
                traceorder="normal",
                itemsizing="constant",
            ),
            **xaxes,
            xaxis_rangeslider_visible=True,
            xaxis_title="Team (Year)",  # Title for the x-axis
        )

        return self.figure
