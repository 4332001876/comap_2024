from hydrologic.base_element import Lake, River

class Config:
    def __init__(self) -> None:     
        # The following are the names of the rivers and lakes in the Great Lakes system
        # high to low, lakes_name = ["clair", "erie", "miHuron", "ontario", "superior"]
        lakes_name = ["superior", "miHuron", "erie", "clair", "ontario"]
        rivers_name = ["detroit", "niagara", "stClair", "stMarys", "stLawrence"]

        # The following are the areas of the lakes in the Great Lakes system
        lakes = {lakes_name[i]: Lake(lakes_name[i], 0, 0) for i in range(len(lakes_name))}

        # area
        lakes["clair"].set_area(1114 * (1000**2))
        lakes["erie"].set_area(25700 * (1000**2))
        lakes["miHuron"].set_area(117620 * (1000**2))
        lakes["ontario"].set_area(18970 * (1000**2))
        lakes["superior"].set_area(82100 * (1000**2))

        # base_height
        lakes["clair"].init_base_height(175.5)
        lakes["erie"].init_base_height(174)
        lakes["miHuron"].init_base_height(176.5)
        lakes["ontario"].init_base_height(74.5)
        lakes["superior"].init_base_height(183.5)

        rivers = {rivers_name[i]: River(rivers_name[i], 0) for i in range(len(rivers_name))}

        # flows of the rivers
        rivers["detroit"].set_new_base(1900, 460)   
        rivers["niagara"].set_new_base(6000, 460)
        rivers["stClair"].set_new_base(1820, 460)
        rivers["stMarys"].set_new_base(10000, 460)
        rivers["stLawrence"].set_new_base(10300, 460)

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

    def get_lakes(self):
        return self.lakes
    
    def get_rivers(self):
        return self.rivers


    
    



