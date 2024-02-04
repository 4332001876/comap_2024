import pandas as pd
import numpy as np
import json

from hydrologic.config import Config

config = Config()
lakes_name = config.lakes_name
rivers_name = config.rivers_name

json_path = "data/stat.json"
json_dict = {}

def get_stat():
    for river_name in rivers_name:
        # get_flow
        json_dict[river_name] = {}
        path = "data/" + river_name + "/%s_flow.csv"%river_name
        flow_df, flow_stat = read_csv_type_month(path)
        print(river_name+" flow: ")
        print(flow_stat)
        json_dict[river_name]["flow"] = flow_stat

    for lake_name in lakes_name:
        # get_water_level
        json_dict[lake_name] = {}
        path = "data/" + lake_name + "/%s_water_level.csv"%lake_name
        water_level_df, water_level_stat = read_csv_type_month(path)
        print(lake_name+" water level: ")
        print(water_level_stat)
        json_dict[lake_name]["water_level"] = water_level_stat

    with open(json_path, "w") as f:
        json.dump(json_dict, f)

    


    

    





def read_csv_type_month(path):
    df = pd.read_csv(path)
    for col in df.columns:
        if col == "Year":
            df[col] = df[col].apply(lambda x: int(x))
        else:
            df[col] = df[col].apply(lambda x: float(x))

    # get average and std of every month
    month_stat = {}
    month_cnt = 1
    for col in df.columns:
        if col != "Year":
            month_stat[month_cnt] = {"mean": df[col].mean(), "std": df[col].std()}
            month_cnt += 1

    return df, month_stat


