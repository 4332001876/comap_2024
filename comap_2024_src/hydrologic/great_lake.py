import numpy as np
import pandas as pd

from hydrologic.config import Config
from hydrologic.base_element import Lake, River, DamController, MosesSaunders, CompensatingWorks

import types

class GreatLake:
    def __init__(self) -> None:
        self.config = Config()
        self.lakes: dict[str, Lake] = self.config.lakes
        self.rivers: dict[str, River] = self.config.rivers

        self.dam_controller = {
            "stMarys": CompensatingWorks(self.rivers["stMarys"]), 
            "stLawrence": MosesSaunders(self.rivers["stLawrence"]),
        }

        self.dt = 60 * 60 * 3 # 3 hours
        
    def run(self, steps):
        for i in range(steps):
            self.update_rivers()
            self.update_lakes()

    def update_lakes(self):
        for lake in self.lakes.values():
            flow = 0
            for river in lake.inflow:
                flow += river.flow
            for river in lake.outflow:
                flow -= river.flow

            amount = flow * self.dt
            lake.add_water(amount)

    def update_rivers(self):
        for river in self.rivers.values():
            river.calc_flow(self.dt)

    def __str__(self) -> str:
        description = ""
        for lake_name in self.config.lakes_name:
            description += str(self.lakes[lake_name]) + ", "
        return description[:-2]
    
    def __repr__(self) -> str:
        return self.__str__()
            







