from dataclasses import dataclass
from enum import Enum
from sys import argv


class Offsets(Enum):
    HEADER_START = 0x00
    HEADER_END = 0x31


class Sizes(Enum):
    HEADER = 50
    COLOUR = 3 # each colour has 3 bytes
    LEVEL = 1
    COUNTRY = 4 # encrypted size
    EQUIPA_SIZE = 1


class EquipaHeaderNotFound(Exception):

    def __init__(self):
        super().__init__('equipa header not found!')


@dataclass
class Player:

    name: str
    position: str
    country: str

    def __repr__(self):
        return f'{self.position}: {self.name} - {self.country}'


@dataclass
class Equipa:

    ext_name: str
    short_name: str
    country: str
    level: int
    colours: list
    coach: str
    players: list

    def __str__(self):
        return (
            f'extended name:\t{self.ext_name}\n'
            f'short name:\t{self.short_name}\n'
            f'country:\t{self.country}\n'
            f'colours:\t{self.colours} (text, background)\n'
            f'level:\t\t{self.level}\n'
            f'coach:\t\t{self.coach}\n'
            f'players:\t{self.players}'
        )


class OffsetCalculator:

    @staticmethod
    def get_short_name(ext_len):
        # +1 to skip the size byte of extended name field
        return Sizes.HEADER.value + ext_len + 1

    @staticmethod
    def get_colours(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        return Sizes.HEADER.value + ext_len + short_len + 2

    @staticmethod
    def get_country(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each colour
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOUR.value * 2 + 4

    @staticmethod
    def get_level(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each colour
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOUR.value * 2 + Sizes.COUNTRY.value + 4

    @staticmethod
    def get_players_number(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each colour
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOUR.value * 2 + Sizes.COUNTRY.value + \
            Sizes.LEVEL.value + 4

    @staticmethod
    def get_players(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each colour
        # +1 to skip to the player nationality
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOUR.value * 2 + Sizes.COUNTRY.value + \
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


class BaseParser:

    def get_field(self, data, offset, size):
        return data[offset:offset+size]

    def decrypt_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            char = (data[i] - data[i - 1]) & 0xff # picking only the 8 less
                                                  # significant bits
            ret += chr(char)

        return ret


class EquipaParser(BaseParser):

    def __init__(self, equipa_file):
        self._file = equipa_file

    def _has_equipa_header(self, data):
        start_offs = Offsets.HEADER_START.value
        end_offs = Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def _parse_ext_name(self, data):
        size = data[Sizes.HEADER.value]
        offs = Sizes.HEADER.value + 1 # skip the 'size' byte

        return self.decrypt_field(data, offs, size)

    def _parse_short_name(self, data, ext_len):
        offs = OffsetCalculator.get_short_name(ext_len)
        size = data[offs]

        return self.decrypt_field(data, offs + 1, size)

    def _parse_colours(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_colours(ext_len, short_len)
        bg = self.get_field(data, offs, Sizes.COLOUR.value)
        txt = self.get_field(data, offs + Sizes.COLOUR.value + 1,
                             Sizes.COLOUR.value)

        return '#' + bg.hex().upper() + ', #' + txt.hex().upper()

    def _parse_level(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_level(ext_len, short_len)
        level = self.get_field(data, offs, Sizes.LEVEL.value)

        return int(level.hex(), 16)

    def _parse_country(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_country(ext_len, short_len)
        country = self.decrypt_field(data, offs, Sizes.COUNTRY.value)

        return country

    def _parse_players(self, data, ext_len, short_len):
        players_offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        pp = PlayersParser(data, players_offs, count_offs)

        return pp.parse()

    def _parse_coach(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_coach(data, ext_len, short_len) + 1
        coach = self.decrypt_field(data, offs, len(data) - offs)

        return coach

    def parse(self):
        with open(self._file, 'rb') as f:
            data = f.read()

            if not self._has_equipa_header(data):
                raise EquipaHeaderNotFound

            ext_name = self._parse_ext_name(data)
            short_name = self._parse_short_name(data, len(ext_name))
            colours = self._parse_colours(data, len(ext_name), len(short_name))
            country = self._parse_country(data, len(ext_name), len(short_name))
            level = self._parse_level(data, len(ext_name), len(short_name))
            players = self._parse_players(data, len(ext_name), len(short_name))
            coach = self._parse_coach(data, len(ext_name), len(short_name))

            return Equipa(ext_name=ext_name, short_name=short_name,
                          country=country, level=level, colours=colours,
                          coach=coach, players=players)


class PlayersParser(BaseParser):

    def __init__(self, data, players_offs, count_offs):
        self._data = data
        self._players_offs = players_offs
        self._count_offs = count_offs

    def _get_player_pos(self, pos_code):
        pos = ''

        match pos_code:
            case 0: pos = 'G'
            case 1: pos = 'Z'
            case 2: pos = 'M'
            case 3: pos = 'A'

        return pos

    def parse(self):
        number_players = self._data[self._count_offs]
        players = []

        for _ in range(0, number_players):
            entry_len = self._data[self._players_offs + Sizes.COUNTRY.value]
            pos_offs = self._players_offs + Sizes.COUNTRY.value + 1 + entry_len
            ret = self.decrypt_field(self._data, self._players_offs,
                                     Sizes.COUNTRY.value + entry_len + 1)

            country = ret[1:4]
            name = ret[5:]
            pos = self._get_player_pos(self._data[pos_offs])

            players.append(Player(name=name, position=pos, country=country))
            # +1 to skip the 'name size' byte
            # +1 to skip the position byte
            # +1 to jump to the next entry
            self._players_offs += Sizes.COUNTRY.value + entry_len + 3

        return players


def main(equipa_file):
    ep = EquipaParser(equipa_file)

    print(ep.parse())


if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        print(f'usage: {argv[0]} <equipa_file>')
