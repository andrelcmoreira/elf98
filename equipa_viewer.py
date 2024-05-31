from dataclasses import dataclass
from enum import Enum
from sys import argv


class EquipaHeaderNotFound(Exception):

    def __init__(self):
        super().__init__('equipa header not found!')


@dataclass
class Player:

    name: str
    position: str
    country: str

    def __str__(self):
        return f'name: {self.name}, position: {self.position}, \
                country: {self.country}'


@dataclass
class Equipa:

    ext_name: str
    short_name: str
    country: str = '' # TODO
    #colours: list = list()
    level: int = 0 # TODO
    coach: str = '' # TODO
    #players: list = list()

    def __str__(self):
        return (
            f'extended name:\t{self.ext_name}\n'
            f'short name:\t{self.short_name}\n'
            f'country:\t{self.country}\n'
            f'level:\t\t{self.level}\n'
            f'coach:\t{self.coach}'
        )


class EquipaParser:

    class Offsets(Enum):
        HEADER_START = 0x00
        HEADER_END = 0x31

    def __init__(self, equipa_file):
        self.file = equipa_file

    def has_equipa_header(self, data):
        start_offs = self.Offsets.HEADER_START.value
        end_offs = self.Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def parse(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if not self.has_equipa_header(data):
                raise EquipaHeaderNotFound

            ext_name = self.parse_ext_name(data)
            short_name = self.parse_short_name(data, len(ext_name))

            return Equipa(ext_name=ext_name, short_name=short_name)

    def parse_ext_name(self, data):
        size = data[self.Offsets.HEADER_END.value + 1]
        data_offs = self.Offsets.HEADER_END.value + 2

        return self.parse_field(data, data_offs, size)

    def parse_short_name(self, data, size_previous):
        size = data[self.Offsets.HEADER_END.value + 2 + size_previous]
        data_offs = self.Offsets.HEADER_END.value + 3

        return self.parse_field(data, data_offs + size_previous, size)

    def parse_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            char = (data[i] - data[i - 1]) & 0xff # picking only the 8 less
                                                  # significant bits
            ret += chr(char)

        return ret


def main(equipa_file):
    ep = EquipaParser(equipa_file)

    print(ep.parse())


if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        print(f'usage: {argv[0]} <equipa_file>')
