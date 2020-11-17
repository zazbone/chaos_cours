from chaos.attractor.Henon import henon
from chaos.attractor.Lozi import lozi
from chaos.attractor.Lorentz import lorentz

from sys import argv

args = argv[1:]

if args[0].lower() == "lorentz":
    lorentz()
elif args[0].lower() == "henon":
    henon()
elif args[0].lower() == "lozi":
    lozi()