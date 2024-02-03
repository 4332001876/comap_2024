import numpy as np
import pandas as pd

from comap_2024_src.hydrologic.config import Config
from comap_2024_src.hydrologic.base_element import Lake, River

import types

class GreatLake:
    def __init__(self) -> None:
        self.config = Config()
        self.lakes: dict[str, Lake] = self.config.lakes
        self.rivers: dict[str, Lake] = self.config.rivers

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
        pass

    def __str__(self) -> str:
        return str(self.lakes)
    
    def __repr__(self) -> str:
        return self.__str__()
            







