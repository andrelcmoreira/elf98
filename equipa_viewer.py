from dataclasses import dataclass
from sys import argv


@dataclass
class Player:

    def __init__(self, name, position, country):
        self.name = name
        self.position = position
        self.country = country

    def __str__(self):
        return f'name: {self.name}, position: {self.position}, \
                country: {self.country}'


class EquipaHeaderNotFound(Exception):

    def __init__(self):
        super().__init__('equipa header not found!')


def has_equipa_header(data):
    return data[0:50] == b'EFa' + b'\x00' * 47


def dump_equipa(data):
    if not has_equipa_header(data):
        raise EquipaHeaderNotFound

    print('team: TODO')
    print('coach: TODO')
    print('score: TODO')
    print('country: TODO')
    print('players: TODO')


def main(equipa_file):
    with open(equipa_file, 'rb') as f:
        data = f.read()

        try:
            dump_equipa(data)
        except EquipaHeaderNotFound as e:
            print(e)


if __name__ == "__main__":
    main(argv[1])
