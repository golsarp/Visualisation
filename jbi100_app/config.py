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

color_list = ["rgb(255,0,0)","rgb(0,0,255)","rgb(0, 200, 0)","rgb(255,0,0,0.4)","rgb(0,0,255,0.4)","rgb(255, 255, 0)","rgb(0, 128, 0)","rgb(128, 128, 128)","rgb(217, 217, 217)","rgb(230, 230, 230)",[0, 0, 255],[255, 0, 0],[0, 255, 0],[255, 165, 0], "rgb(255,153,0)"]
color_red_blind = [
                "rgb(255, 0, 0)",          # Red
                "rgb(0, 102, 204)",        # Blue (adjusted for better visibility)
                "rgb(204, 204, 204)",        # Green (adjusted for better visibility)
                "rgba(255, 0, 0, 0.4)",    # Transparent Red
                "rgba(0, 102, 204, 0.4)",  # Transparent Blue (adjusted for better visibility)
                "rgb(255, 255, 0)",        # Yellow
                "rgb(0, 102, 0)",          # Dark Green (adjusted for better visibility)
                "rgb(128, 128, 128)",      # Gray
                "rgb(204, 204, 204)",      # Light Gray (adjusted for better visibility)
                "rgb(217, 217, 217)",      # Light Gray
                [0, 51, 204],              # Dark Blue (adjusted for better visibility)
                [255, 77, 77],             # Salmon (adjusted for better visibility)
                [0, 204, 0],               # Bright Green
                [255, 153, 51],             # Orange (adjusted for better visibility)
                "rgb(255,153,0)",
            ]

color_list_random = [
                "rgb(178, 34, 34)",         # Firebrick (adjusted for better visibility)
                "rgb(0, 102, 204)",         # Blue
                "rgb(0, 128, 0)",           # Green (adjusted for better visibility)
                "rgba(178, 34, 34, 0.4)",   # Transparent Firebrick (adjusted for better visibility)
                "rgba(0, 102, 204, 0.4)",   # Transparent Blue
                "rgb(255, 255, 0)",         # Yellow
                "rgb(0, 102, 0)",           # Dark Green
                "rgb(128, 128, 128)",       # Gray
                "rgb(204, 204, 204)",       # Light Gray
                "rgb(217, 217, 217)",       # Light Gray
                [0, 51, 204],               # Dark Blue
                [255, 77, 77],              # Salmon
                [0, 204, 0],                # Bright Green
                [255, 153, 51],             # Orange
                "rgb(255,153,0)",
            ]


   # 0 home color , 1 away color , 2 field color , 3 home bench color,  4 away bench color , 5 selected player color, 6 fiedl gird color, 7 selected bench , 8 bench non editable, 9 bench title, 10-11-12-13
      



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
