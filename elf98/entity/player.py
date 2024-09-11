from dataclasses import dataclass


@dataclass
class Player:

    name: str
    position: str
    country: str
    appearances: int = 0

    def __repr__(self) -> str:
        return f'{self.position}: {self.name} - {self.country}'
