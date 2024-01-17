# Here you can add any global configuations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
position_mapping_home = {"GK": 1, "DF": 2, "MF": 4, "FW": 6}

position_mapping_away = {"GK": 13, "DF": 12, "MF": 10, "FW": 8}

player_poss_path = (
    "FIFA DataSet/Data/FIFA World Cup 2022 Player Data/player_possession.csv"
)
formation = ["4-3-3-1", "5-3-2-1", "4-4-2-1", "3-5-2-1"]

GK = 1
DF = 2
MF = 4
FW = 6


def swap_players(home_selected_field, home_selected_bench, home_bench, player_dataf):
    drop_columns = ["position_x", "position_y"]

    # get the row of bench player
    home_b_pl_data = home_bench[home_bench["player"] == home_selected_bench]

    # bench values
    bench_poss = home_b_pl_data[["position_x", "position_y"]]

    # drop bench positions
    home_b_pl_data_dropped = home_b_pl_data.drop(columns=drop_columns)

    # get the player value on field
    home_field_pl_data = player_dataf[player_dataf["player"] == home_selected_field]

    drop_field = ["position_x", "position_y", "corrected_y", "color"]

    # pos values of field player
    field_pos = home_field_pl_data[["position_x", "position_y", "corrected_y", "color"]]

    home_field_pl_data = home_field_pl_data.drop(columns=drop_field)

    # new bench player going into the field
    home_b_pl_data_dropped[drop_field] = field_pos.values

    home_field_pl_data[drop_columns] = bench_poss.values

    # get bench player in field
    player_dataf.loc[home_field_pl_data.index] = home_b_pl_data_dropped.values

    # field player to bench
    home_bench.loc[home_b_pl_data.index] = home_field_pl_data.values

    # return home_selected_field, home_selected_bench
    return player_dataf, home_bench
