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
    country: str
    level: int
    colours: list
    coach: str # TODO
    players: list # TODO

    def __str__(self):
        return (
            f'extended name:\t{self.ext_name}\n'
            f'short name:\t{self.short_name}\n'
            f'country:\t{self.country}\n'
            f'level:\t\t{self.level}\n'
            f'coach:\t{self.coach}\n'
            f'colours:\t{self.colours} (text, background)\n'
            f'players:\t{self.players}'
        )


class EquipaParser:

    class Offsets(Enum):
        HEADER_START = 0x00
        HEADER_END = 0x31

    class Sizes(Enum):
        HEADER = 50
        COLOUR = 3 # each colour has 3 bytes
        LEVEL = 1
        COUNTRY = 4

    def __init__(self, equipa_file):
        self.file = equipa_file

    def _has_equipa_header(self, data):
        start_offs = self.Offsets.HEADER_START.value
        end_offs = self.Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def _get_field(self, data, offset, size):
        return data[offset:offset+size]

    def _decrypt_field(self, data, offset, size):
        ret = ''

        for i in range(offset, offset + size):
            char = (data[i] - data[i - 1]) & 0xff # picking only the 8 less
                                                  # significant bits
            ret += chr(char)

        return ret

    def _get_short_name_offset(self, ext_len):
        # +1 to skip the size byte of extended name field
        return self.Sizes.HEADER.value + ext_len + 1

    def _get_colours_offset(self, ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        return self.Sizes.HEADER.value + ext_len + short_len + 2

    def _get_country_offset(self, ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields and +2 to
        # skip the apparently unused 1 byte on each colour
        return self.Sizes.HEADER.value + ext_len + short_len + \
            self.Sizes.COLOUR.value * 2 + 4

    def _get_level_offset(self, ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields, +2 to
        # skip the apparently unused 1 byte on each colour
        return self.Sizes.HEADER.value + ext_len + short_len + \
            self.Sizes.COLOUR.value * 2 + self.Sizes.COUNTRY.value + 4

    def parse_ext_name(self, data):
        size = data[self.Offsets.HEADER_END.value + 1]
        data_offs = self.Offsets.HEADER_END.value + 2 # skip the 'size' byte

        return self._decrypt_field(data, data_offs, size)

    def parse_short_name(self, data, ext_len):
        offset = self._get_short_name_offset(ext_len)
        size = data[offset]

        return self._decrypt_field(data, offset + 1, size)

    def parse_colours(self, data, ext_len, short_len):
        offset = self._get_colours_offset(ext_len, short_len)
        bg = self._get_field(data, offset, self.Sizes.COLOUR.value)
        txt = self._get_field(data, offset + self.Sizes.COLOUR.value + 1,
                              self.Sizes.COLOUR.value)
        colours = '#' + bg.hex().upper() + ', #' + txt.hex().upper()

        return colours

    def parse_level(self, data, ext_len, short_len):
        offset = self._get_level_offset(ext_len, short_len)
        level = self._get_field(data, offset, self.Sizes.LEVEL.value)

        return int(level.hex(), 16)

    def parse_country(self, data, ext_len, short_len):
        offset = self._get_country_offset(ext_len, short_len)
        country = self._decrypt_field(data, offset, self.Sizes.COUNTRY.value)

        return country

    def parse(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if not self._has_equipa_header(data):
                raise EquipaHeaderNotFound

            ext_name = self.parse_ext_name(data)
            short_name = self.parse_short_name(data, len(ext_name))
            colours = self.parse_colours(data, len(ext_name), len(short_name))
            country = self.parse_country(data, len(ext_name), len(short_name))
            level = self.parse_level(data, len(ext_name), len(short_name))
            coach = ''
            players = []

            return Equipa(ext_name=ext_name, short_name=short_name,
                          country=country, level=level, colours=colours,
                          coach=coach, players=players)


def main(equipa_file):
    ep = EquipaParser(equipa_file)

    print(ep.parse())


if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        print(f'usage: {argv[0]} <equipa_file>')
