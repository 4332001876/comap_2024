from hydrologic.great_lake import GreatLake
from hydrologic.get_statistic import get_stat, get_NBS_stat
from hydrologic.rating_curve import get_rating_curve


from cybernetic.mpc import MpcController

def test_great_lake():
    gl = GreatLake()
    print(gl)
    for _ in range(10):
        gl.run(48)
        print(gl.date.ctime())
        print(gl)
    print("MSE Loss at", gl.date.ctime(), ":", gl.calc_mse_loss())

def test_mpc():
    gl = GreatLake()
    mpc = MpcController(gl)
    mpc.run(480)
    print("MSE Loss at", gl.date.ctime(), ":", gl.calc_mse_loss())

def test_get_stat():
    #get_stat()
    #get_NBS_stat()
    get_rating_curve()

if __name__ == "__main__":
    # test_get_stat()
    test_great_lake()
    test_mpc()

