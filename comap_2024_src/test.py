from hydrologic.great_lake import GreatLake

def test_great_lake():
    gl = GreatLake()
    print(gl)
    gl.run(10)
    print(gl)


if __name__ == "__main__":
    test_great_lake()