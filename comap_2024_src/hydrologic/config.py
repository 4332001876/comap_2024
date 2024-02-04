from hydrologic.base_element import Lake, River

class Config:
    def __init__(self) -> None:     
        # The following are the names of the rivers and lakes in the Great Lakes system
        # high to low, lakes_name = ["clair", "erie", "miHuron", "ontario", "superior"]
        lakes_name = ["superior", "miHuron", "erie", "clair", "ontario"]
        rivers_name = ["detroit", "niagara", "stClair", "stMarys", "stLawrence"]

        # The following are the areas of the lakes in the Great Lakes system
        lakes = {lakes_name[i]: Lake(lakes_name[i]) for i in range(len(lakes_name))}

        # area (from wiki)
        lakes["clair"].set_area(1114 * (1000**2))
        lakes["erie"].set_area(25700 * (1000**2))
        lakes["miHuron"].set_area(117620 * (1000**2))
        lakes["ontario"].set_area(18970 * (1000**2))
        lakes["superior"].set_area(82100 * (1000**2))

        # geogian bay: 15000 km^2; huron: 59590 km^2; huron without geogian bay: 44590 km^2; michigan: 58030 km^2

        rivers = {rivers_name[i]: River(rivers_name[i]) for i in range(len(rivers_name))}

        # connect the rivers and lakes
        lakes["superior"].append_outflow(rivers["stMarys"])
        rivers["stMarys"].append_upstream_lake(lakes["superior"])

        rivers["stMarys"].append_downstream_lake(lakes["miHuron"])
        lakes["miHuron"].append_inflow(rivers["stMarys"])

        lakes["miHuron"].append_outflow(rivers["stClair"])
        rivers["stClair"].append_upstream_lake(lakes["miHuron"])

        rivers["stClair"].append_downstream_lake(lakes["clair"])
        lakes["clair"].append_inflow(rivers["stClair"])

        lakes["clair"].append_outflow(rivers["detroit"])
        rivers["detroit"].append_upstream_lake(lakes["clair"])

        rivers["detroit"].append_downstream_lake(lakes["erie"])
        lakes["erie"].append_inflow(rivers["detroit"])

        lakes["erie"].append_outflow(rivers["niagara"])
        rivers["niagara"].append_upstream_lake(lakes["erie"])

        rivers["niagara"].append_downstream_lake(lakes["ontario"])
        lakes["ontario"].append_inflow(rivers["niagara"])

        lakes["ontario"].append_outflow(rivers["stLawrence"])
        rivers["stLawrence"].append_upstream_lake(lakes["ontario"])

        self.lakes = lakes
        self.rivers = rivers

        self.lakes_name = lakes_name
        self.rivers_name = rivers_name

        self.path_config = PathConfig()

    def get_lakes(self):
        return self.lakes
    
    def get_rivers(self):
        return self.rivers

class PathConfig:
    def __init__(self) -> None:
        self.data_path = "data/"
        self.result_path = "result/"
        self.model_path = "model/"

        self.stat_path = "data/stat.json"
        self.nbs_stat_path = "data/nbs_stat.json"
    
    



