from dataclasses import dataclass


@dataclass
class Color:

    text: str
    background: str

    def __str__(self):
        return '#' + self.background.hex().upper() + ', #' \
            + self.text.hex().upper()
