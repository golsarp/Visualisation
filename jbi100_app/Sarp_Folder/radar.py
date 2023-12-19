import plotly.graph_objects as go
import pandas as pd
import plotly.graph_objects as go


player_names = ["Cristiano Ronaldo", "Aaron Ramsey", "Abdelhamid Sabiri"]
path_poss = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
path_shoot = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_shooting.csv"
path_pass = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_passing.csv"
df_poss = pd.read_csv(path_poss)
df_shoot = pd.read_csv(path_shoot)
df_pass = pd.read_csv(path_pass)

attributes = [
    ("dribbles_completed_pct", df_poss),
    ("passes_pct_short", df_pass),
    ("passes_pct_long", df_pass),
    ("passes_pct_medium", df_pass),
    ("shots_on_target_pct", df_shoot),
]
# print(df_poss["dribbles_completed_pct"])
# print(df_pass["passes_pct_short"])
# print(df_pass["passes_pct_long"])
# print(df_pass["passes_pct_medium"])
# print(df_shoot["shots_on_target_pct"])
r_extend = []
for player in player_names:
    print("player :", player)
    player_r = []
    for i, att_info in enumerate(attributes):
        # print(i, att_info[0])
        df = att_info[1]
        player_df = df[df["player"] == player]
        # Extract the value of the 'dribbles_completed_pct' column
        att_val = player_df[att_info[0]].values[0]
        print("att_val", att_val)
        player_r.append(att_val)
    r_extend.append(player_r)

print("r is ", r_extend)
fig = go.Figure()
categories = [
    "dribbles_completed_pct",
    "passes_pct_short",
    "passes_pct_long",
    "passes_pct_medium",
    "shots_on_target_pct",
]

for i in range(len(player_names)):
    fig.add_trace(
        go.Scatterpolar(
            r=r_extend[i],
            theta=categories,
            # fill="toself",
            name=player_names[i],
        )
    )
# # fig.add_trace(
# #     go.Scatterpolar(
# #         r=[4, 3, 2.5, 1, 2], theta=categories, fill="toself", name="Product B"
# #     )
# # )

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
)

fig.show()
