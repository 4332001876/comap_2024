import types

class Lake:
    def __init__(self, name, area, base_height) -> None:
        # const
        self.name = name
        self.area = area
        self.base_height = base_height

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

    def set_best_water_level(self, water_level) -> None:
        self.best_water_level = water_level

    def __str__(self) -> str:
        return f"Lake {self.name} at {self.water_level} m"
    
    def __repr__(self) -> str:
        return self.__str__()


class River:
    def __init__(self, name, flow) -> None:
        # const
        self.name = name

        # var
        self.flow = flow
        self.best_flow = flow

        
        self.upstream_lake : list[Lake] = [] # 上游湖泊
        self.downstream_lake :list[Lake]= []  # 下游湖泊

    def set_flow(self, flow) -> None:
        self.flow = flow

    def set_best_flow(self, flow) -> None:
        self.best_flow = flow

    def append_upstream_lake(self, lake):
        self.upstream_lake.append(lake)

    def append_downstream_lake(self, lake):
        self.downstream_lake.append(lake)

    def __str__(self) -> str:
        return f"River {self.name} at {self.flow} m^3/s"
    
    def __repr__(self) -> str:
        return self.__str__()
















