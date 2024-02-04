from hydrologic.great_lake import GreatLake
from cybernetic.mpc import MpcController

def test_great_lake():
    gl = GreatLake()
    print(gl)
    for _ in range(1):
        gl.run(100)
        print(gl)

def test_mcp():
    gl = GreatLake()
    mcp = MpcController(gl)
    mcp.run(100)

if __name__ == "__main__":
    test_mcp()
    test_great_lake()