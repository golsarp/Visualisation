import plotly.express as px
import pandas as pd
from config import position_mapping_home, position_mapping_away, player_poss_path


# df = px.data.medals_long()
# sort = df[df["medal"] == "gold"]
# df_2 = px.data.iris()
# combined_df = pd.concat([df_2["species"], sort], ignore_index=True)
df = pd.read_csv(player_poss_path)
unique_teams_count = df["team"].unique()[:5]
print(unique_teams_count)
# break


# print(combined_df)
def process_df(team, home):
    df = pd.read_csv(player_poss_path)
    df_team = df[df["team"] == team].copy()
    df_team = df_team.sort_values(by="position")
    mapping = position_mapping_home if home else position_mapping_away

    df_team["position_x"] = df_team["position"].map(mapping)
    df_team["position_y"] = df_team.groupby("position").cumcount() + 1
    return df_team


# file_path = player_poss_path
# df = pd.read_csv(file_path)
# print(df)
df_home = process_df("Australia", True)
df_away = process_df("Brazil", False)
df_concat = pd.concat([df_home, df_away], ignore_index=True)

# df_home = df[df["team"] == "Australia"].copy()
# # print(df_home)
# # print("***" * 15)
# # df_home["position"] = df_home["position"].map(position_mapping)
# # df_home["position"] = df_home["position"]
# # position_counts = df_home.groupby("position").size().reset_index(name="count")

# df_home = df_home.sort_values(by="position")
# df_home["position_x"] = df_home["position"].map(position_mapping_home)

# df_home["position_y"] = df_home.groupby("position").cumcount() + 1
# print(df_home)
# df_home_sorted["position"] = df_home_sorted["position_x"].map(position_mapping)

# print(df_home)
# df_away = df[df["team"] == "Brazil"].copy()
# df_away = df_away.sort_values(by="position")
# df_away["position_x"] = df_away["position"].map(position_mapping_away)

# df_away["position_y"] = df_away.groupby("position").cumcount() + 1
# # print(df_away)
# result = pd.concat([df_home, df_away], ignore_index=True)

# print(result)
# df = px.data.medals_long()
# print(df)

# fig = px.scatter(
#     df_concat, y="position_y", x="position_x", color="position", symbol="position"
# )

# # Add annotations (text on top of values)
# for i, row in df_concat.iterrows():
#     fig.add_annotation(
#         x=row["position_x"],  # x-coordinate of the annotation
#         y=row["position_y"],  # y-coordinate of the annotation
#         # name=row["player"],
#         text=str(row["player"]),  # text to display
#         # showarrow=True,
#         # arrowhead=2,
#         # arrowcolor="black",
#         # arrowsize=1,
#         # arrowwidth=2,
#         ax=0,
#         ay=-40,
#     )

# fig.update_traces(marker_size=10)
# fig.show()
