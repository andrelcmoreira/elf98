from dataclasses import dataclass
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
    country: str = ''
    #colours: list = list()
    level: int = 0
    coach: str = ''
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

    def __init__(self, equipa_file):
        self.file = equipa_file

    def has_equipa_header(self, data):
        return data[0:50] == b'EFa' + b'\x00' * 47

    def parse(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if not self.has_equipa_header(data):
                raise EquipaHeaderNotFound

            ext_name = self.parse_ext_name(data)
            short_name = self.parse_short_name(data, len(ext_name))

            return Equipa(ext_name=ext_name, short_name=short_name)

    def parse_ext_name(self, data):
        size = data[50]

        return self.parse_field(data, 51, size)

    def parse_short_name(self, data, size_previous):
        size = data[51 + size_previous]

        return self.parse_field(data, 52 + size_previous, size)

    def parse_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            char = (data[i] - data[i - 1]) & 0xff
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
