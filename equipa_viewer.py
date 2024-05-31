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
    #country: str = ''
    #colours: list = list()
    #coach: str = ''
    #level: int = 0
    #players: list = list()

    def __str__(self):
        #return f'''
        #    name: {self.full_name}
        #    abrev. name: {self.short_name}
        #    level: {self.level}
        #    country: {self.country}
        #    coach: {self.coach}
        #    players: {self.players}
        #    '''
        return f'''extended name: {self.ext_name}, short name: {self.short_name}'''


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

            size_ext_name = data[50]
            ext_name = self.parse_field(data, 51, size_ext_name)

            size_short_name = data[51 + size_ext_name]
            short_name = self.parse_field(data, 52 + size_ext_name,
                                          size_short_name)

            return Equipa(ext_name=ext_name, short_name=short_name)

    def parse_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            char = (data[i] - data[i-1]) & 0xff
            ret += chr(char)

        return ret

def main(equipa_file):
    equipa = EquipaParser(equipa_file).parse()

    print(equipa)


if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        print(f'usage: {argv[0]} <equipa_file>')
