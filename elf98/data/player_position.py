from enum import Enum


class PlayerPosition(Enum):
    G = 0 # goalkeeper
    D = 1 # defender
    M = 2 # midfielder
    A = 3 # forward ('atacante' in portuguese)
