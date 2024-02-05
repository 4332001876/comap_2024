from hydrologic.great_lake import GreatLake
from hydrologic.get_statistic import get_stat, get_NBS_stat, get_2017_flow_nbs, get_2017_ontario
from hydrologic.rating_curve import get_rating_curve


from cybernetic.mpc import MpcController

def test_great_lake():
    gl = GreatLake()
    print(gl)
    for _ in range(5):
        gl.run(48)
        # print(gl.date.ctime())
        # print(gl)
    print(gl.date.ctime())
    print(gl)
    print("MSE Loss at", gl.date.ctime(), ":", gl.calc_mse_loss())

def test_mpc():
    gl = GreatLake()
    mpc = MpcController(gl)
    mpc.run(48*5)
    print("MSE Loss at", gl.date.ctime(), ":", gl.calc_mse_loss())

def test_get_stat():
    #get_stat()
    #get_NBS_stat()
    get_rating_curve()
    # get_2017_flow_nbs()

if __name__ == "__main__":
    # test_get_stat()
    # test_great_lake()
    # test_mpc()
    get_2017_ontario()
    

