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

        # self.reservoir_limit = 0
        # self.reservoir_water = 0
        
        self.upstream_lake : list[Lake] = [] # 上游湖泊
        self.downstream_lake :list[Lake]= []  # 下游湖泊

    def calc_flow(self, flow) -> None:
        if len(self.upstream_lake) == 0:
            self.flow = flow + np.random.normal(0, self.std)
        self.flow = self.base_flow + self.std * self.upstream_lake[0].get_normalized_water_level()

    def set_new_base(self, flow, std) -> None:
        self.base_flow = flow
        self.std = std

    def set_flow(self, flow) -> None:
        self.flow = flow

    def append_upstream_lake(self, lake):
        self.upstream_lake.append(lake)

    def append_downstream_lake(self, lake):
        self.downstream_lake.append(lake)

    def __str__(self) -> str:
        flow_str = "%.4f" % self.flow
        return f"River {self.name} at {flow_str} m^3/s"
    
    def __repr__(self) -> str:
        return self.__str__()

class DamController:
    def __init__(self, river:River) -> None:
        self.river = river
        self.upstream_lake = river.upstream_lake[0]

        self.is_winter = False

        self.legal_action_num = 20

        """
        （以圣劳伦斯河为例）
        f_limit(flood_limit): 洪水限制，，其为分层阈值，
        i_limit(ice_limit): 冰冻限制，冰盖未形成时为6230，形成后为9430
        j_limit(change_rate_limit): 周平均流量最大变化量，为700 m3/s，This limit increases to 1,420 m3/s if Lake Ontario levels exceed 75.2 m and ice is not forming in the St. Lawrence River. 
        l_limit(max_limit): 10,700 m3/s if the Lake Ontario level should rise above 76.0 m during the navigation season and 11,500 m3/s during the non-navigation season
        m_limit(min_limit):
        """

    def get_legal_action(self):
        # change_rate_limit = self.get_change_rate_limit()
        max_limit = self.get_max_limit()
        min_limit = self.get_min_limit()
        if max_limit >= min_limit:
            legal_action = np.linspace(min_limit, max_limit, self.legal_action_num)
        else:
            legal_action = np.linspace(max_limit, min_limit, self.legal_action_num)

        return legal_action

    def control(self, flow):
        max_limit = self.get_max_limit()
        min_limit = self.get_min_limit()
        if (flow-max_limit)*(flow-min_limit) < 0:
            self.river.set_flow(flow)


class MosesSaunders(DamController):
    def __init__(self, river:River) -> None:
        super().__init__(river)
        '''
            self.flood_limit
            self.ice_limit
            self.change_rate_limit
            self.max_limit
            self.min_limit
        '''

    def get_change_rate_limit(self):
        level = self.upstream_lake.water_level
        if level > 75.2:
            return 1420
        else:
            return 700
    
    def get_max_limit(self):
        level = self.upstream_lake.water_level
        max_limit = 10700
        if level < 74.22:
            max_limit = 5950
        elif level < 74.34:
            max_limit = 5950 + 1333*(level - 74.22)
        elif level < 74.54:
            max_limit = 6111 + 9100*(level - 74.34)
        elif level < 74.70:
            max_limit = 7930 + 2625*(level - 74.54)
        elif level < 75.13:
            max_limit = 8350 + 1000*(level - 74.70)
        elif level < 75.44:
            max_limit = 8780 + 3645*(level - 75.13)
        elif level < 75.70:
            max_limit = 9910
        elif level < 76.00:
            max_limit = 10200   
        else:
            max_limit = 10700

        channel_capacity = 747.2 * (level - 69.10)**1.47
        if max_limit > channel_capacity:
            max_limit = channel_capacity

        # ice_limit 
        if self.is_winter:
            max_limit = 6230

        return max_limit
    
    def get_min_limit(self):
        level = self.upstream_lake.water_level
        if level > 74.2:
            return 6800
        elif level > 74.1:
            return 6500
        elif level > 74.0:
            return 6200
        elif level > 73.6:
            return 6100
        else:
            return 5770
        



class CompensatingWorks(DamController):
    def __init__(self, river:River) -> None:
        super().__init__(river)
   
    def get_max_limit(self):
        return 3000
    
    def get_min_limit(self):
        return 1400




