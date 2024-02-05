import pandas as pd
import numpy as np
import json
import calendar

from hydrologic.config import Config
from hydrologic.base_element import Lake, River
from hydrologic.great_lake import GreatLake

config = Config()
lakes_name = config.lakes_name
rivers_name = config.rivers_name
gl = GreatLake()

json_path = config.path_config.stat_path
nbs_json_path = config.path_config.nbs_stat_path

def get_stat():
    json_dict = {}
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

    """with open(json_path, "w") as f:
        json.dump(json_dict, f)"""

    
def get_NBS_stat():
    json_dict = {}
    river_dict = {}
    lake_dict = {}
    for river_name in rivers_name:
        # get_flow
        path = "data/" + river_name + "/%s_flow.csv"%river_name
        flow_df, _ = read_csv_type_month(path)
        # select lines between 2012 and 2020
        flow_df = flow_df[(flow_df["Year"] >= 2012) & (flow_df["Year"] <= 2020)]
        flow_vector = flow_df.iloc[:, 1:].values.flatten()
        flow_vector = flow_vector[:-1] # 除去最后一个月的数据
        river_dict[river_name] = flow_vector


    for lake_name in lakes_name:
        # get_water_level
        json_dict[lake_name] = {}
        path = "data/" + lake_name + "/%s_water_level.csv"%lake_name
        water_level_df, _ = read_csv_type_month(path)
        # select lines between 2012 and 2020
        water_level_df = water_level_df[(water_level_df["Year"] >= 2012) & (water_level_df["Year"] <= 2020)]

        # v = area * water_level
        volumn_matrix = gl.lakes[lake_name].area * water_level_df.iloc[:, 1:].values
        # flatten the matrix (in time order)
        volumn = volumn_matrix.flatten()
        volumn_diff = volumn[1:] - volumn[:-1] 
        # diff to change rate
        for i in range(0, len(volumn_diff)):
            year = i // 12 + 2012
            month = i % 12 + 1
            days_in_month = calendar.monthrange(year, month)[1]
            # print(days_in_month)
            volumn_diff[i] = volumn_diff[i] / (days_in_month * 24 * 3600)

        lake_dict[lake_name] = volumn_diff # volumn_change_rate

    # cal NBS: inflow - outflow + NBS = volumn_change_rate -> NBS = volumn_change_rate - inflow + outflow
    # print(lake_dict)
    # print(river_dict)

    for lake_name in lakes_name:
        lake = gl.lakes[lake_name]
        NBS = lake_dict[lake_name]
        for river in lake.inflow:
            NBS -= river_dict[river.name]
        for river in lake.outflow:
            NBS += river_dict[river.name]

        '''
        # pearson-correlation-coefficient
        x = NBS[:-1]
        y = NBS[1:]
        pearson = np.corrcoef(x, y)
        print(lake_name + " pearson-correlation-coefficient: ", pearson)
        '''
        
        month_data = {i+1:[NBS[j*12+i] for j in range(8)] for i in range(12)}
        NBS_stat = {}
        for month, data in month_data.items():
            NBS_stat[month] = {"mean": np.mean(data), "std": np.std(data)}
        json_dict[lake_name]["NBS"] = NBS_stat

    """with open(nbs_json_path, "w") as f:
        json.dump(json_dict, f)"""

    

    

    





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


def read_csv_glerl(path):
    # NOAA/GLERL Large Lake Thermodynamics Model
    df = pd.read_csv(path, skiprows=3)
    for col in df.columns:
        if col == "YYYY":
            df[col] = df[col].apply(lambda x: int(x))
        else:
            df[col] = df[col].apply(lambda x: float(x))
    return df

def get_glerl_stat(df):
    # get average and std of every month
    month_stat = {}
    month_cnt = 1
    for col in df.columns:
        if col != "YYYY":
            month_stat[month_cnt] = {"mean": df[col].mean(), "std": df[col].std()}
            month_cnt += 1
    return month_stat



