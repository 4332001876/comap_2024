import numpy as np
import pandas as pd
import json
import datetime

from hydrologic.config import Config
from hydrologic.base_element import Lake, River, DamController, MosesSaunders, CompensatingWorks

import types

class GreatLake:
    def __init__(self, date: datetime.datetime = datetime.datetime(2017, 1, 1, 0, 0, 0)) -> None:
        self.config = Config()
        self.lakes: dict[str, Lake] = self.config.lakes
        self.rivers: dict[str, River] = self.config.rivers

        self.dam_controller = {
            "stMarys": CompensatingWorks(self.rivers["stMarys"]), 
            "stLawrence": MosesSaunders(self.rivers["stLawrence"]),
        }

        self.date: datetime.datetime = date
        self.month = self.date.month
        self.start_new_month(self.month)

        self.dt = 60 * 30 # s, 0.5 hours
        self.daily_discount_rate = 0.5
        # self.dt_nbs_std_factor = np.sqrt(30 * np.log(1 / self.daily_discount_rate)) * (self.dt / 86400) * np.log(1 / self.daily_discount_rate)
        self.dt_nbs_std_factor = np.sqrt(30 * (86400 / self.dt))
        self.alpha = self.daily_discount_rate ** (self.dt /86400)
        # print("alpha: ", self.alpha)
        # print("dt_nbs_std_factor: ", self.dt_nbs_std_factor)

    def start_new_month(self, month: int):
        month = str(month)
        stat = json.load(open(self.config.path_config.stat_path))
        nbs_stat = json.load(open(self.config.path_config.nbs_stat_path))
        for lake in self.lakes.values():
            base_height = stat[lake.name]["water_level"][month]["mean"]
            std = stat[lake.name]["water_level"][month]["std"]
            nbs_mean = nbs_stat[lake.name]["NBS"][month]["mean"]
            nbs_std = nbs_stat[lake.name]["NBS"][month]["std"]
            lake.set_new_base(base_height, std, nbs_mean, nbs_std)
            lake.set_best_water_level(base_height)
        for river in self.rivers.values():
            base_flow = stat[river.name]["flow"][month]["mean"]
            std_flow = stat[river.name]["flow"][month]["std"]
            river.set_new_base(base_flow, std_flow)
        
    def run(self, steps, dam_action: dict[str, float] = {}):
        for i in range(steps):
            self.update_rivers()
            for dam_name, action in dam_action.items():
                self.dam_controller[dam_name].set_action(action)
            self.update_lakes()
            
            self.date += datetime.timedelta(seconds=self.dt)
            if self.date.month != self.month:
                self.month = self.date.month
                self.start_new_month(self.month)

    def calc_mse_loss(self):
        mse_loss = 0
        for lake in self.lakes.values():
            mse_loss += (lake.water_level - lake.best_water_level) ** 2
        return mse_loss

    def update_lakes(self):
        for lake in self.lakes.values():
            change_rate = 0
            for river in lake.inflow:
                change_rate += river.flow
            for river in lake.outflow:
                change_rate -= river.flow
            new_nbs = lake.nbs_mean + lake.nbs_std * self.dt_nbs_std_factor * np.random.normal() 
            lake.last_nbs = self.alpha * lake.last_nbs + (1 - self.alpha) * new_nbs
            # print(lake.last_nbs)
            change_rate += lake.last_nbs
            amount = change_rate * self.dt
            lake.add_water(amount)

    def update_rivers(self):
        for river in self.rivers.values():
            river.calc_flow(self.alpha, self.dt_nbs_std_factor)

    def __str__(self) -> str:
        description = ""
        for lake_name in self.config.lakes_name:
            description += str(self.lakes[lake_name]) + ", "
        return description[:-2]
    
    def __repr__(self) -> str:
        return self.__str__()
            







