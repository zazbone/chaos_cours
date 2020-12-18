from three_body import main
from json import load


with open("solar_sys.json") as f:
    config = load(f)


main(config)