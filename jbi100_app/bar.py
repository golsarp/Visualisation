import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


position_mapping_home = {"GK": 1, "DF": 2, "MF": 4, "FW": 6}
position_mapping_away = {"GK": 13, "DF": 12, "MF": 10, "FW": 8}


file_path = "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
formation = ["4-2-3-1", "5-3-2-1", "4-4-2-1", "4-2-3-1", "4-1-4-1"]


def process_df(team, home):
    df = pd.read_csv(file_path)
    df_team = df[df["team"] == team].copy()
    df_team = df_team.sort_values(by="position")
    mapping = position_mapping_home if home else position_mapping_away

    df_team["position_x"] = df_team["position"].map(mapping)
    df_team["position_y"] = df_team.groupby("position").cumcount() + 1

    return df_team


df = process_df("Wales", True)
# print("whole team")
# print(df.shape[0])
# print(df)


def select_players(df, formation):
    positions = formation.split("-")
    positions = list(map(int, positions))
    # print("pos", positions)

    selected_players = pd.DataFrame()
    unselected_players = pd.DataFrame()

    i = 0
    for pos in positions:
        # print("pos ", pos)
        position_df = df[
            df["position"].str.startswith(
                "FW" if i == 0 else "MF" if i == 1 else "DF" if i == 2 else "GK"
            )
        ]

        selected_players = pd.concat([selected_players, position_df.head(pos)])
        unselected_players = pd.concat([unselected_players, position_df.tail(-pos)])
        if len(position_df) < pos:
            print("pos ", pos)
            p = pos - len(position_df)
            # Handle the case where there are fewer than 'pos' players
            print("less than formation ", pos - len(position_df))
            # print(unselected_players)
            # random_players = unselected_players.sample(n=p, replace=True)
            # print("random players ")
            # print(random_players)
            # selected_players = pd.concat([selected_players, random_players])

        i += 1

    return selected_players, unselected_players


# Example usage:
selected_players, bench = select_players(
    df, formation[1]
)  # Change the index to select a different formation
print("selecetd ")
max_val = selected_players["position_y"].max()


def calculate_corrected_y(group, max_val):
    # You can customize the factor as needed
    factor = max_val / (len(group) + 1)
    print("factor ", len(group) + 1)
    print("group ", group)
    # group["numeric_y"] = pd.to_numeric(group["position_y"], errors="coerce")
    res = group["position_y"] * factor
    # print("res is ", res)
    # print("gorup after ")
    # group["res"] = group["position_y"] * factor

    group["corrected_y"] = group["position_y"] * factor
    # print("gorup after ")
    # print(group)

    return group["corrected_y"]


# factor = max_val / (selected_players.groupby("position").size() + 1)
# print("factor ", factor)
# selected_players["corrected_y"] = (
#     selected_players.groupby("position")
#     .apply(calculate_corrected_y, max_val=max_val)
#     .reset_index(drop=True)
# )

selected_players["corrected_y"] = (
    selected_players.groupby("position")
    .apply(lambda group: calculate_corrected_y(group, max_val))
    .reset_index(level=0, drop=True)
)


# selected_players.groupby("position")

print(selected_players)
# print("bench ")
# print(bench)
