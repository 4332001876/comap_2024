from hydrologic.great_lake import GreatLake
from hydrologic.get_statistic import get_stat, get_NBS_stat


from cybernetic.mpc import MpcController

def test_great_lake():
    gl = GreatLake()
    print(gl)
    for _ in range(365):
        gl.run(48)
        print(gl.date.ctime())
        print(gl)

def test_mcp():
    gl = GreatLake()
    mcp = MpcController(gl)
    mcp.run(100)

def test_get_stat():
    #get_stat()
    get_NBS_stat()

if __name__ == "__main__":
    test_get_stat()
    # test_great_lake()
