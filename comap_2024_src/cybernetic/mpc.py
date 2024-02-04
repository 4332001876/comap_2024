import copy
import gc

from hydrologic.great_lake import GreatLake


class MpcController:
    def __init__(self, great_lake: GreatLake) -> None:
        self.great_lake = great_lake

        self.SIM_STEPS = 2

    def run_one_step(self):
        best_loss = float("inf")
        legal_action = [dam.get_legal_action() for dam in self.great_lake.dam_controller.values()]
        assert len(legal_action) == 2
        # dam1: stMarys; dam2: stLawrence
        for action1 in legal_action[0]:
            for action2 in legal_action[1]:
                great_lake_copy = copy.deepcopy(self.great_lake)
                great_lake_copy.dam_controller["stMarys"].set_action(action1)
                great_lake_copy.dam_controller["stLawrence"].set_action(action2)
                great_lake_copy.run(self.SIM_STEPS)
                loss = great_lake_copy.calc_mse_loss()
                # print(loss, action1, action2)
                if loss < best_loss:
                    best_loss = loss
                    best_action = (action1, action2)
        best_action = {dam_name: action for dam_name, action in zip(self.great_lake.dam_controller.keys(), best_action)}
        # print(best_action)
        self.great_lake.run(1, best_action)

    def run(self, steps):
        for i in range(steps):
            self.run_one_step()
            if i % 100 == 99:
                print(self.great_lake)
            gc.collect()
        print("MPC finished")
        print(self.great_lake.date.ctime())
        print(self.great_lake)


