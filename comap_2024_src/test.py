from hydrologic.great_lake import GreatLake

def test_great_lake():
    gl = GreatLake()
    print(gl)
    for _ in range(10):
        gl.run(9999)
        print(gl)


if __name__ == "__main__":
    test_great_lake()