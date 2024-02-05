import numpy as np
import pandas as pd
import json
import datetime

from hydrologic.config import Config
from hydrologic.base_element import Lake, River, DamController, MosesSaunders, CompensatingWorks

import types

IS_2017 = True
if IS_2017:
    with open("data/flow_2017.json", "r") as f:
        flow_2017 = json.load(f)
    nbs_2017 = {'superior': [1029.89781360454, 1073.527502025648, 3049.7169836984594, 7018.487096407408, 5369.825631836786, 4933.519967284705, 4076.906945046595, 3804.36087369773, 2998.3489421604936, 2042.3630159534052, 1030.330378037037, 103.23974955794529], 'miHuron': [3736.0729048040625, 5649.1782213439155, 9162.095144452807, 9984.00098876543, 7492.791412432497, 8629.17127017284, 3503.025278804062, 18.19994837156446, 882.0490398148158, 2290.369286391875, 579.0588108148149, 1170.3608491756277], 'clair': [547.6659475663082, 541.9369862962958, 482.62814239784893, 445.2788300864195, 199.36876756630863, 153.21283403703728, 28.670151911589528, -47.43201817682166, 5.059613925925987, 226.71140495579493, 325.241200950617, 247.4164667347668], 'erie': [1287.3594511099163, 1124.7207162592595, 1843.5316529880529, 2381.214566222223, 1251.3758966463556, 837.1206198641976, 
-151.99843310991673, -384.83011810991684, -754.4853736790128, 244.3734969999996, -267.9174268395054, -127.18492687813614], 'ontario': [1326.2229757752966, 1582.5503313334339, 3416.2352556069295, 4200.534842777777, 1330.8295601887703, 2144.1398992592585, 1380.8091790920862, 973.3763833929788, 1409.3020483086411, 2097.46324718877, 801.6016590493828, 2148.3252031326156]}

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
            
    def set_2017(self, month):
        month = str(month)
        stat = json.load(open(self.config.path_config.stat_path))
        nbs_stat = json.load(open(self.config.path_config.nbs_stat_path))
        for lake in self.lakes.values():
            base_height = stat[lake.name]["water_level"][month]["mean"]
            std = stat[lake.name]["water_level"][month]["std"]
            nbs_mean = nbs_2017[lake.name][int(month) - 1]
            nbs_std = nbs_stat[lake.name]["NBS"][month]["std"]
            lake.set_new_base(base_height, std, nbs_mean, nbs_std)
            lake.set_best_water_level(base_height)
        for river in self.rivers.values():
            base_flow = flow_2017[river.name]["flow"][month]["mean"]
            std_flow = stat[river.name]["flow"][month]["std"]
            river.set_new_base(base_flow, std_flow)
    
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
        if IS_2017:
            self.set_2017(month)
        
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
            







