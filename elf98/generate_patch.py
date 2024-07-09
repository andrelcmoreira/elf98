from sys import argv
from dataclasses import dataclass
from enum import Enum


class Offsets(Enum):
    HEADER_START = 0x00
    HEADER_END = 0x31


class Sizes(Enum):
    HEADER = 50
    COLOR = 3 # each color has 3 bytes
    LEVEL = 1
    COUNTRY = 4 # encrypted size
    EQUIPA_SIZE = 1


class OffsetCalculator:

    @staticmethod
    def get_extended_name():
        # +1 to skip the size byte
        return Sizes.HEADER.value + 1

    @staticmethod
    def get_short_name(ext_len):
        # +1 to skip the size byte of extended name field
        return Sizes.HEADER.value + ext_len + 1

    @staticmethod
    def get_colors(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        return Sizes.HEADER.value + ext_len + short_len + 2

    @staticmethod
    def get_country(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + 4

    @staticmethod
    def get_level(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + 4

    @staticmethod
    def get_players_number(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + \
            Sizes.LEVEL.value + 4

    @staticmethod
    def get_players(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each color
        # +1 to skip to the player nationality
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + \
            Sizes.LEVEL.value + Sizes.EQUIPA_SIZE.value + 5

    @staticmethod
    def get_coach(data, ext_len, short_len):
        offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        number_players = data[count_offs]

        for _ in range(0, number_players):
            entry_len = data[offs + Sizes.COUNTRY.value]
            # +1 to skip the 'name size' byte
            # +1 to skip the position byte
            # +1 to jump to the next entry
            offs += Sizes.COUNTRY.value + entry_len + 3

        return offs


class EquipaParser:

    def __init__(self, equipa_file):
        self._file = equipa_file

    @staticmethod
    def parse_ext_name(data):
        offs = OffsetCalculator.get_extended_name()
        size = data[Sizes.HEADER.value]

        return decrypt(data, offs, size)

    @staticmethod
    def parse_short_name(data, ext_len):
        offs = OffsetCalculator.get_short_name(ext_len)
        size = data[offs]

        return decrypt(data, offs + 1, size)


@dataclass
class Player:

    name: str
    position: str
    country: str

    def __repr__(self):
        return f'{self.position}: {self.name} - {self.country}'


COACH = 'Luis Zubeldia'
# https://www.espn.com.br/futebol/time/elenco/_/id/2026/bra.sao_paulo
PLAYERS = [
    Player(name='Rafael', position='G', country='BRA'),
    Player(name='Jandrei', position='G', country='BRA'),
    Player(name='Igor', position='Z', country='BRA'),
    Player(name='Diego Costa', position='Z', country='BRA'),
    Player(name='Robert Arboleda', position='Z', country='EQU'),
    Player(name='Wellington', position='Z', country='BRA'),
    Player(name='Alan Franco', position='Z', country='ARG'),
    Player(name='Nahuel Ferraresi', position='Z', country='VNZ'),
    Player(name='Michel Araújo', position='M', country='URU'),
    Player(name='Giuliano Galoppo', position='M', country='ARG'),
    Player(name='Rodrigo Nestor', position='M', country='BRA'),
    Player(name='Luiz Gustavo', position='M', country='BRA'),
    Player(name='Alisson', position='M', country='BRA'),
    Player(name='Welington Rato', position='M', country='BRA'),
    Player(name='James Rodriguez', position='M', country='COL'),
    Player(name='Lucas Moura', position='A', country='BRA'),
    Player(name='Jonathan Calleri', position='A', country='ARG'),
    Player(name='Luciano', position='A', country='BRA'),
    Player(name='Ferreira', position='A', country='BRA'),
    Player(name='Juan', position='A', country='BRA'),
    Player(name='Erick', position='A', country='BRA'),
    Player(name='André Silva', position='A', country='BRA'),
]


def decrypt(data, offset, size):
    ret = ''

    for i in range(offset, offset + size):
        ret += chr((data[i] - data[i - 1]) & 0xff)

    return ret


def to_pos_code(pos):
    match pos:
        case 'G': return 0
        case 'Z': return 1
        case 'M': return 2
        case 'A': return 3


def encrypt(text):
    out = bytearray()

    out.append(len(text))
    for i in range(0, len(text)):
        out.append((ord(text[i]) + out[i]) & 0xff)

    return out


def add_players(file):
    player = bytearray()

    for entry in PLAYERS:
        player.append(int(0))
        player += encrypt(entry.country)
        player += encrypt(entry.name)
        player.append(to_pos_code(entry.position))

        file.write(player)

        player.clear()


def add_coach(file):
    coach = bytearray()

    coach.append(int(0))
    coach += encrypt(COACH)

    file.write(coach)


def add_player_number(file):
    file.write(len(PLAYERS).to_bytes())


def create_base_equipa(in_file, out_file):
    with open(in_file, 'r+b') as f:
        data = f.read()

        ext_name = EquipaParser.parse_ext_name(data)
        short_name = EquipaParser.parse_short_name(data, len(ext_name))
        offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

        out_file.write(data[:offs + 1])


def update_equipa(in_file, out_file):
    with open(out_file, 'ab') as f:
        create_base_equipa(in_file, f)
        add_player_number(f)
        add_players(f)
        add_coach(f)


def main(in_file, out_file):
    update_equipa(in_file, out_file)


# TODO: fetch the player list
# TODO: remove duplicated codes
main(argv[1], argv[2])
