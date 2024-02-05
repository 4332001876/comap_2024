import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import statsmodels.api as sm

from hydrologic.config import Config
from hydrologic.base_element import Lake, River
from hydrologic.great_lake import GreatLake

from hydrologic.get_statistic import read_csv_type_month

config = Config()
lakes_name = config.lakes_name
rivers_name = config.rivers_name
gl = GreatLake()


def get_rating_curve():
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
        river_dict[river_name] = flow_vector


    for lake_name in lakes_name:
        # get_water_level
        json_dict[lake_name] = {}
        path = "data/" + lake_name + "/%s_water_level.csv"%lake_name
        water_level_df, _ = read_csv_type_month(path)
        # select lines between 2012 and 2020
        water_level_df = water_level_df[(water_level_df["Year"] >= 2012) & (water_level_df["Year"] <= 2020)]

        # v = area * water_level
        water_level = water_level_df.iloc[:, 1:].values.flatten()
        lake_dict[lake_name] = water_level # volumn_change_rate

    # linear regression
    for river_name in rivers_name:
        river = gl.rivers[river_name]
        if len(river.upstream_lake) == 0:
            continue

        flow_vector = river_dict[river_name]
        high = lake_dict[river.upstream_lake[0].name]
        if len(river.downstream_lake) == 0:
            low = 0
        else:
            low = lake_dict[river.downstream_lake[0].name]
        X = high - np.mean(low)
        # X = np.log(X)
        # Y = np.log(flow_vector)
        Y = flow_vector
        plotting(X, Y)

        X = sm.add_constant(X)
        model = sm.OLS(Y, X)
        results = model.fit()
        print(river_name)
        print(results.summary())




def plotting(X, Y):
    plt.scatter(X, Y)
    plt.show()









