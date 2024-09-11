from enum import Enum


class PlayerPosition(Enum):
    G = 0 # goalkeeper
    D = 1 # defender
    M = 2 # midfielder
    A = 3 # forward ('atacante' in portuguese)

    @staticmethod
    def to_pos_code(pos: str) -> int:
        match pos:
            case PlayerPosition.G.name: return PlayerPosition.G.value
            case PlayerPosition.D.name: return PlayerPosition.D.value
            case PlayerPosition.M.name: return PlayerPosition.M.value
            case PlayerPosition.A.name: return PlayerPosition.A.value

    @staticmethod
    def to_pos_name(pos_code: int) -> str:
        match pos_code:
            case PlayerPosition.G.value: return PlayerPosition.G.name
            case PlayerPosition.D.value: return PlayerPosition.D.name
            case PlayerPosition.M.value: return PlayerPosition.M.name
            case PlayerPosition.A.value: return PlayerPosition.A.name
