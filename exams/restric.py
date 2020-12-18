from three_body import main
from json import load


with open("restric.json") as f:
    config = load(f)


main(config)