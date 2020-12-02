import chaos

from pathlib import Path
from json import load, dump


MOD_PATH = Path(chaos.__file__).parent
USER_PATH = Path()


class Config:
    def __init__(self, json_path=""):
        if json_path:
            json_path = Path(json_path).with_suffix(".json")
            with open(json_path, "r") as json_conf:
                conf = load(json_conf)
                self.config_name = Path(json_path).with_suffix("")

        else:
            with open(MOD_PATH / "_config.json", "r") as json_conf:
                conf = load(json_conf)
                self.config_name = Path("out")

        self.dim = conf["dimensions"]
        self.sample = 1 << int(conf["sample_power"])
        self.keeped_sample = 1 << int(conf["keep_sample_pow"])
        self.tf = float(conf["duration(s)"])
        self.G = float(conf["G"])

        self.get_pos = conf["yield"]["position"]
        self.get_speed = conf["yield"]["speed"]
        self.get_acc = conf["yield"]["acceleration"]

        self.b_name = [b["name"] for b in conf["parameters"].values()]
        self.b_mass = [b["mass"] for b in conf["parameters"].values()]
        self.b_pos = [b["position"] for b in conf["parameters"].values()]
        self.b_speed = [b["speed"] for b in conf["parameters"].values()]


def new_config_file(path="out.json"):
    with open(MOD_PATH / "_config.json", "r") as json_defaut:
        default_config = load(json_defaut)

    path = Path(path).with_suffix(".json")
    if path.is_absolute:
        with open(path, "w") as new_config:
            dump(default_config, new_config, indent=4)
    else:
        with open(path, "w") as new_config:
            dump(default_config, new_config, indent=4)
