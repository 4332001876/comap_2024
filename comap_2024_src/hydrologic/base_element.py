import types
from typing import Any

import numpy as np

class Lake:
    def __init__(self, name, area, base_height, std = 0.15) -> None:
        # const
        self.name = name
        self.area = area
        self.base_height = base_height
        self.std = std

        # var
        self.water_level = base_height
        self.best_water_level = base_height
        self.inflow: list[River]= []
        self.outflow: list[River] = []

    def add_water(self, amount):
        self.water_level += amount / self.area

    def append_inflow(self, river):
        self.inflow.append(river)

    def append_outflow(self, river):
        self.outflow.append(river)


    def get_normalized_water_level(self):
        return (self.water_level - self.base_height) / self.std
    # getter

    # setter
    def init_base_height(self, base_height) -> None:
        self.base_height = base_height
        self.water_level = base_height
        self.best_water_level = base_height

    def set_new_base(self, base_height, std) -> None:
        self.base_height = base_height
        self.std = std

    def set_area(self, area) -> None:
        self.area = area

    def set_best_water_level(self, water_level) -> None:
        self.best_water_level = water_level

    def __str__(self) -> str:
        water_level_str = "%.4f" % self.water_level
        return f"Lake {self.name} at {water_level_str} m"
    
    def __repr__(self) -> str:
        return self.__str__()


class River:
    def __init__(self, name, flow, std=500) -> None:
        # const
        self.name = name

        # var
        self.flow = flow
        self.std = std
        self.base_flow = flow

        self.reservoir_limit = 0
        self.reservoir_water = 0
        
        self.upstream_lake : list[Lake] = [] # 上游湖泊
        self.downstream_lake :list[Lake]= []  # 下游湖泊

    def calc_flow(self, flow) -> None:
        if len(self.upstream_lake) == 0:
            self.flow = flow + np.random.normal(0, self.std)
        self.flow = self.base_flow + self.std * self.upstream_lake[0].get_normalized_water_level()

    def control_flow(self, declined_flow) -> None:
        pass

    def set_new_base(self, flow, std) -> None:
        self.base_flow = flow
        self.std = std

    def append_upstream_lake(self, lake):
        self.upstream_lake.append(lake)

    def append_downstream_lake(self, lake):
        self.downstream_lake.append(lake)

    def __str__(self) -> str:
        flow_str = "%.4f" % self.flow
        return f"River {self.name} at {flow_str} m^3/s"
    
    def __repr__(self) -> str:
        return self.__str__()
















