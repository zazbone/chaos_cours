from three_body import main as m1
from planet import main as m2

from json import load


with open("moore.json") as f:
    config2 = load(f)
m1(config2)

with open("solar_sys.json") as f:
    config1 = load(f)
m1(config1)



m2()