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


# https://www.espn.com.br/futebol/time/elenco/_/id/2026/bra.sao_paulo
PLAYERS = [
    Player(name='Rafael', position='G', country='BRA'),
    Player(name='Jandrei', position='G', country='BRA'),
    Player(name='Igor', position='Z', country='BRA'),
    Player(name='Diego Costa', position='Z', country='BRA'),
    Player(name='Robert Arboleda', position='Z', country='EQU'),
    Player(name='Wellington', position='Z', country='BRA'),
    Player(name='Alan Franco', position='Z', country='ARG'),
    Player(name='Michel Araújo', position='M', country='URU'),
    Player(name='Giuliano Galoppo', position='M', country='ARG'),
    Player(name='Rodrigo Nestor', position='M', country='BRA'),
    Player(name='Luiz Gustavo', position='M', country='BRA'),
    Player(name='Lucas Moura', position='A', country='BRA'),
    Player(name='Jonathan Calleri', position='A', country='ARG'),
    Player(name='Luciano', position='A', country='BRA'),
    Player(name='Ferreira', position='A', country='BRA'),
    Player(name='Juan', position='A', country='BRA'),
    Player(name='Erick', position='A', country='BRA'),
]
COACH = 'Luis Zubeldia'


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
    out = []

    out.append(len(text).to_bytes())

    for i in range(0, len(text)):
        out.append(((ord(text[i]) + int.from_bytes(out[i])) & 0xff).to_bytes())

    return out


def update_players(file):
    with open(file, 'ab') as f:
        for player in PLAYERS:
            country = encrypt(player.country)
            name = encrypt(player.name)

            f.write(int(0).to_bytes())
            for ch in country:
                f.write(ch)

            for ch in name:
                f.write(ch)

            f.write(to_pos_code(player.position).to_bytes())


def update_coach(file):
    with open(file, 'ab') as f:
        name = encrypt(COACH)

        f.write(int(0).to_bytes())
        for ch in name:
            f.write(ch)


def update_player_number(file):
    with open(file, 'r+b') as f:
        data = f.read()

        ext_name = EquipaParser.parse_ext_name(data)
        short_name = EquipaParser.parse_short_name(data, len(ext_name))

        offs = OffsetCalculator.get_players_number(len(ext_name),
                                                   len(short_name))

        f.seek(offs)
        f.write(len(PLAYERS).to_bytes())


def main(file):
    update_player_number(file)
    update_players(file)
    update_coach(file)


main(argv[1])
