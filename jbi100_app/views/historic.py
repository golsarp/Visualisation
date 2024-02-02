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
        """
        This function builds the historical data visualization for two teams.

        Parameters:
        team1 (str): The name of the first team.
        team2 (str): The name of the second team.
        colors (list): A list of colors to be used in the visualization.

        Returns:
        go.Figure: Plotly figure object with the historical data visualization.
        """

        # Load the data from the CSV file
        df = pd.read_csv(file_path)

        # Convert the "Year" column to integer type
        df["Year"] = df["Year"].astype(int)

        # Create an empty figure
        self.figure = go.Figure()

        # Extract home scores for team 1
        home_scores_by_year_team1 = df[df["home_team"] == team1][
            ["Year", "home_score", "away_score", "away_team", "home_team"]
        ]

        # Determine if team 1 won the match when playing at home
        home_scores_by_year_team1["is_winner"] = (
                home_scores_by_year_team1["home_score"]
                > home_scores_by_year_team1["away_score"]
        )

        # Drop the "away_score" column
        home_scores_by_year_team1 = home_scores_by_year_team1.drop(
            columns=["away_score"]
        )

        # Extract home scores for team 2 from the dataframe
        home_scores_by_year_team2 = df[df["home_team"] == team2][
            ["Year", "home_score", "away_score", "away_team", "home_team"]
        ]

        # Add a new column "is_winner" to the dataframe.
        # This column is True if team 2 won the match when playing at home,
        # and False otherwise.
        home_scores_by_year_team2["is_winner"] = (
            home_scores_by_year_team2["home_score"]
            > home_scores_by_year_team2["away_score"]
        )

        # Drop the "away_score" column from the dataframe as it is no longer needed
        home_scores_by_year_team2 = home_scores_by_year_team2.drop(
            columns=["away_score"]
        )

        # Extract away scores for team 1 from the dataframe
        away_scores_by_year_team1 = df[df["away_team"] == team1][
            ["Year", "away_score", "home_score", "home_team", "away_team"]
        ]

        # Add a new column "is_winner" to the dataframe.
        # This column is True if team 1 won the match when playing away, and False otherwise.
        away_scores_by_year_team1["is_winner"] = (
            away_scores_by_year_team1["away_score"]
            > away_scores_by_year_team1["home_score"]
        )

        # Drop the "home_score" column from the dataframe as it is no longer needed
        away_scores_by_year_team1 = away_scores_by_year_team1.drop(
            columns=["home_score"]
        )

        # Extract away scores for team 2 from the dataframe
        away_scores_by_year_team2 = df[df["away_team"] == team2][
            ["Year", "away_score", "home_score", "home_team", "away_team"]
        ]

        # Add a new column "is_winner" to the dataframe. This column is True if team 2 won the match when playing away,
        # and False otherwise.
        away_scores_by_year_team2["is_winner"] = (
            away_scores_by_year_team2["away_score"]
            > away_scores_by_year_team2["home_score"]
        )

        # Drop the "home_score" column from the dataframe as it is no longer needed
        away_scores_by_year_team2 = away_scores_by_year_team2.drop(
            columns=["home_score"]
        )

        # Concatenate home and away scores for team 1
        # This creates a new dataframe that contains all the scores for team 1,
        # regardless of whether the match was played at home or away.
        scores_by_year_team1 = pd.concat(
            [home_scores_by_year_team1, away_scores_by_year_team1]
        )

        # Sort the scores by year
        # This ensures that the scores are displayed in chronological order.
        scores_by_year_team1 = scores_by_year_team1.sort_values("Year")

        # Concatenate home and away scores for team 2
        # This creates a new dataframe that contains all the scores for team 2,
        # regardless of whether the match was played at home or away.
        scores_by_year_team2 = pd.concat(
            [home_scores_by_year_team2, away_scores_by_year_team2]
        )

        # Sort the scores by year
        # This ensures that the scores are displayed in chronological order.
        scores_by_year_team2 = scores_by_year_team2.sort_values("Year")

        # Get a list of unique years from both teams' scores
        # This list will be used to create the x-axis of the plot.
        unique_years = list(
            set(scores_by_year_team1["Year"]).union(set(scores_by_year_team2["Year"]))
        )

        # Sort the years
        # This ensures that the years on the x-axis are displayed in chronological order.
        unique_years.sort()

        def get_color(is_home_team, is_home, is_winner):
            """
            This function determines the color to be used for a team based on whether the team is playing at home or away,
            and whether the team won the match.

            Parameters:
            is_home_team (bool): A boolean indicating whether the team is the home team.
            is_home (bool): A boolean indicating whether the match is being played at home.
            is_winner (bool): A boolean indicating whether the team won the match.

            Returns:
            str: A string representing the color in rgba format.
            """

            # Define the base color for home and away
            # If the team is the home team, the base colors are set to colors[11] and colors[12]
            # If the team is the away team, the base colors are set to colors[10] and colors[13]
            if is_home_team:
                base_color_home = colors[11]     # Red  10,11,12,13
                base_color_away = colors[12]     # Green
            else:
                base_color_home = colors[10]     # Blue
                base_color_away = colors[13]     # Orange

            # The color is set to the base home color if the match is being played at home,
            # and to the base away color otherwise
            color = base_color_home if is_home else base_color_away

            # If the team won the match, the color is set to a fully opaque version of the base color
            # If the team lost the match, the color is set to a semi-transparent version of the base color
            if is_winner:
                adjusted_color = "rgba({}, {}, {}, {})".format(
                    int(color[0]), int(color[1]), int(color[2]), 1
                )
            else:
                adjusted_color = "rgba({}, {}, {}, {})".format(
                    int(color[0]), int(color[1]), int(color[2]), 0.5
                )

            # The function returns the adjusted color
            return adjusted_color

        # Initialize a dictionary to track whether the legend item has been added for each score type (home and away)
        # for team 1 and team 2
        legend_added_team1 = {"Home Score": False, "Away Score": False}
        legend_added_team2 = {"Home Score": False, "Away Score": False}

        # Iterate over the dataframe containing home scores for team 1
        for index, row in home_scores_by_year_team1.iterrows():
            # Initialize a variable to determine whether to show the legend for this trace
            show_legend = False
            # If the legend for home scores of team 1 has not been added yet,
            # set show_legend to True and update the dictionary
            if not legend_added_team1["Home Score"]:
                show_legend = True
                legend_added_team1["Home Score"] = True

            # If the home score for the current row is NaN or the home team is not team 1, skip this iteration
            if pd.isna(row["home_score"]) or row["home_team"] != team1:
                continue

            # Adding a trace to the figure for the home scores of team 1
            self.figure.add_trace(
                # Creating a bar chart
                go.Bar(
                    # The x-axis represents the home team and the year of the match
                    x=[f"{row['home_team']} ({row['Year']})"],
                    # The y-axis represents the home score
                    y=[row["home_score"]],
                    # The name of the trace is "Home Scores For" followed by the name of the home team
                    name="Home Scores For " + str(row["home_team"]),
                    # The color of the bar is determined by the get_color function
                    # The first argument is True because the team is the home team
                    # The second argument is True because the match is being played at home
                    # The third argument is the value of the "is_winner" column for the current row
                    marker_color=get_color(True, True, row["is_winner"]),
                    # The hover info is set to "y+text" to display the y value and
                    # the hover text when hovering over the bar
                    hoverinfo="y+text",
                    # The hover text is "Won Against" followed by the name of the away team
                    # if the home team won the match,
                    # and "Lost Against" followed by the name of the away team otherwise
                    hovertext="Won Against " + str(row["away_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["away_team"]),
                    # The legend is shown if show_legend is True
                    showlegend=show_legend,
                    # The legend group is set to "Home Scores Team 1"
                    legendgroup="Home Scores Team 1",
                )
            )

        # Iterating over the dataframe containing away scores for team 1
        for index, row in away_scores_by_year_team1.iterrows():
            # Initialize a variable to determine whether to show the legend for this trace
            show_legend = False
            # If the legend for away scores of team 1 has not been added yet,
            # set show_legend to True and update the dictionary
            if not legend_added_team1["Away Score"]:
                show_legend = True
                legend_added_team1["Away Score"] = True

            # If the away score for the current row is NaN or the away team is not team 1, skip this iteration
            if pd.isna(row["away_score"]) or row["away_team"] != team1:
                continue

            # Adding a trace to the figure for the away scores of team 1
            self.figure.add_trace(
                # Creating a bar chart
                go.Bar(
                    # The x-axis represents the away team and the year of the match
                    x=[f"{row['away_team']} ({row['Year']})"],
                    # The y-axis represents the away score
                    y=[row["away_score"]],
                    # The name of the trace is "Away Scores For" followed by the name of the away team
                    name="Away Scores For " + str(row["away_team"]),
                    # The color of the bar is determined by the get_color function
                    # The first argument is True because the team is the home team
                    # The second argument is False because the match is not being played at home
                    # The third argument is the value of the "is_winner" column for the current row
                    marker_color=get_color(True, False, row["is_winner"]),
                    # The hover info is set to "y+text" to display the y value and the hover text
                    # when hovering over the bar
                    hoverinfo="y+text",
                    # The hover text is "Won Against" followed by the name of the home team
                    # if the away team won the match,
                    # and "Lost Against" followed by the name of the home team otherwise
                    hovertext="Won Against " + str(row["home_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["home_team"]),
                    # The legend is shown if show_legend is True
                    showlegend=show_legend,
                    # The legend group is set to "Away Scores Team 1"
                    legendgroup="Away Scores Team 1",
                )
            )

        # Iterating over the dataframe containing home scores for team 2
        for index, row in home_scores_by_year_team2.iterrows():
            # Initialize a variable to determine whether to show the legend for this trace
            show_legend = False
            # If the legend for home scores of team 2 has not been added yet,
            # set show_legend to True and update the dictionary
            if not legend_added_team2["Home Score"]:
                show_legend = True
                legend_added_team2["Home Score"] = True

            # If the home score for the current row is NaN or the home team is not team 2, skip this iteration
            if pd.isna(row["home_score"]) or row["home_team"] != team2:
                continue

            # Adding a trace to the figure for the home scores of team 2
            self.figure.add_trace(
                # Creating a bar chart
                go.Bar(
                    # The x-axis represents the home team and the year of the match
                    x=[f"{row['home_team']} ({row['Year']})"],
                    # The y-axis represents the home score
                    y=[row["home_score"]],
                    # The name of the trace is "Home Scores For" followed by the name of the home team
                    name="Home Scores For " + str(row["home_team"]),
                    # The color of the bar is determined by the get_color function
                    # The first argument is False because the team is not the home team
                    # The second argument is True because the match is being played at home
                    # The third argument is the value of the "is_winner" column for the current row
                    marker_color=get_color(False, True, row["is_winner"]),
                    # The hover info is set to "y+text" to display the y value and the hover text
                    # when hovering over the bar
                    hoverinfo="y+text",
                    # The hover text is "Won Against" followed by the name of the away team
                    # if the home team won the match,
                    # and "Lost Against" followed by the name of the away team otherwise
                    hovertext="Won Against " + str(row["away_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["away_team"]),
                    # The legend is shown if show_legend is True
                    showlegend=show_legend,
                    # The legend group is set to "Home Scores Team 2"
                    legendgroup="Home Scores Team 2",
                )
            )

        # This block of code is responsible for adding traces for away scores of team 2 to the figure.
        # It iterates over the dataframe containing away scores for team 2.

        # For each row in the dataframe:
        for index, row in away_scores_by_year_team2.iterrows():
            # Initialize a variable to determine whether to show the legend for this trace.
            # By default, it is set to False.
            show_legend = False

            # If the legend for away scores of team 2 has not been added yet,
            # set show_legend to True and update the dictionary.
            # This ensures that the legend is only added once for away scores of team 2.
            if not legend_added_team2["Away Score"]:
                show_legend = True
                legend_added_team2["Away Score"] = True

            # If the away score for the current row is NaN (Not a Number) or the away team is not team 2,
            # skip this iteration. This is done to avoid adding traces for matches that are not relevant
            # or for which the score is not available.
            if pd.isna(row["away_score"]) or row["away_team"] != team2:
                continue

            # Adding a trace to the figure for the away scores of team 2
            self.figure.add_trace(
                # Creating a bar chart
                go.Bar(
                    # The x-axis represents the away team and the year of the match
                    x=[f"{row['away_team']} ({row['Year']})"],
                    # The y-axis represents the away score
                    y=[row["away_score"]],
                    # The name of the trace is "Away Scores For" followed by the name of the away team
                    name="Away Scores For " + str(row["away_team"]),
                    # The color of the bar is determined by the get_color function
                    # The first argument is False because the team is not the home team
                    # The second argument is False because the match is not being played at home
                    # The third argument is the value of the "is_winner" column for the current row
                    marker_color=get_color(False, False, row["is_winner"]),
                    # The hover info is set to "y+text" to display the y value and the hover text
                    # when hovering over the bar
                    hoverinfo="y+text",
                    # The hover text is "Won Against" followed by the name of the home team
                    # if the away team won the match,
                    # and "Lost Against" followed by the name of the home team otherwise
                    hovertext="Won Against " + str(row["home_team"])
                    if row["is_winner"]
                    else "Lost Against " + str(row["home_team"]),
                    # The legend is shown if show_legend is True
                    showlegend=show_legend,
                    # The legend group is set to "Away Scores Team 2"
                    legendgroup="Away Scores Team 2",
                )
            )

        # Initialize empty lists for ordered_categories, tickvals, and ticktext
        ordered_categories = []
        tickvals = []
        ticktext = []

        # Iterate over the unique_years list with the enumerate function,
        # which returns both the index (i) and the value (year)
        for i, year in enumerate(unique_years):
            # Append a formatted string to the ordered_categories list. The string contains the team name and the year.
            ordered_categories.append(f"{team1} ({year})")
            ordered_categories.append(f"{team2} ({year})")

            # Append the index multiplied by 2 plus 0.5 to the tickvals list.
            # This value will be used for positioning the ticks on the x-axis.
            tickvals.append(i * 2 + 0.5)

            # Append the year as a string to the ticktext list.
            # This value will be used as the label for the ticks on the x-axis.
            ticktext.append(str(year))

        # Creating a dictionary for the x-axis configuration
        xaxes = {
            # The key is "xaxis" which represents the x-axis
            "xaxis": dict(
                # The domain of the x-axis is set to [0, 1], which means it spans the entire width of the plot
                domain=[0, 1],
                # The anchor is set to "y", which means the position of the x-axis is determined by the y-axis
                anchor="y",
                # showticklabels is set to True, which means the tick labels are displayed
                showticklabels=True,
                # fixedrange is set to True, which means the range of the x-axis is fixed and cannot be zoomed or panned
                fixedrange=True,
                # tickmode is set to "array", which means the tick values are set manually using
                # the tickvals and ticktext arrays
                tickmode="array",
                # tickvals is set to the previously defined tickvals list, which determines the positions of the ticks
                tickvals=tickvals,
                # ticktext is set to the previously defined ticktext list, which determines the labels of the ticks
                ticktext=ticktext,
                # categoryorder is set to "array", which means the categories (teams and years)
                # are ordered according to the categoryarray
                categoryorder="array",
                # categoryarray is set to the previously defined ordered_categories list,
                # which determines the order of the categories
                categoryarray=ordered_categories,
            )
        }

        # Annotation for the x-axis title
        annotations = [
            dict(
                # The x-coordinate of the annotation's position in normalized coordinates (from 0 to 1)
                x=0.5,
                # The y-coordinate of the annotation's position in normalized coordinates (from 0 to 1)
                y=-0.1,
                # The text of the annotation. Here it is an empty string, which means no text will be displayed
                text="",
                # This specifies whether an arrow should be displayed from the annotation to a point on the plot.
                # Here it is set to False, which means no arrow will be displayed
                showarrow=False,
                # This specifies the reference system for the 'x' key. Here it is set to 'paper',
                # which means the 'x' value is in normalized coordinates
                xref="paper",
                # This specifies the reference system for the 'y' key. Here it is set to 'paper',
                # which means the 'y' value is in normalized coordinates
                yref="paper",
                # This specifies the font of the annotation text.
                # It is a dictionary with the key 'size' specifying the font size
                font=dict(size=15),
                # This specifies the part of the annotation that is positioned at the 'x' coordinate.
                # Here it is set to 'center', which means the center of the annotation
                # is positioned at the 'x' coordinate
                xanchor="center",
                # This specifies the part of the annotation that is positioned at the 'y' coordinate.
                # Here it is set to 'top', which means the top of the annotation is positioned at the 'y' coordinate
                yanchor="top",
            )
        ]

        # Custom layout
        self.figure.update_layout(
            barmode="stack",  # Set the mode for bar chart to stack
            title=f"{team1} and {team2} Historical Scores by Year",  # Set the title of the chart
            yaxis_title="Score",  # Set the title for y-axis
            yaxis=dict(fixedrange=True),  # Set the range of y-axis as fixed
            annotations=annotations,  # Add annotations to the chart
            margin=dict(l=50, r=50, t=50, b=50),  # Set the margin of the chart
            # Configure the legend of the chart
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
            **xaxes,  # Add the x-axis configuration
            xaxis_rangeslider_visible=True,  # Make the range slider for x-axis visible
            xaxis_title="Team (Year)",  # Set the title for x-axis
        )

        return self.figure  # Return the figure object
