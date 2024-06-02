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
    country: str # TODO
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
        COLOUR = 3
        LEVEL = 1

    def __init__(self, equipa_file):
        self.file = equipa_file

    def _has_equipa_header(self, data):
        start_offs = self.Offsets.HEADER_START.value
        end_offs = self.Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def _get_short_name_offset(self, ext_len):
        return self.Offsets.HEADER_END.value + ext_len + 2

    def _get_colours_offset(self, ext_len, short_len):
        return self.Offsets.HEADER_END.value + ext_len + short_len + 3

    def _get_level_offset(self, ext_len, short_len):
        return self.Offsets.HEADER_END.value + ext_len + short_len + \
            self.Sizes.COLOUR.value + 12

    def parse(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if not self._has_equipa_header(data):
                raise EquipaHeaderNotFound

            ext_name = self._parse_ext_name(data)
            short_name = self._parse_short_name(data,
                self._get_short_name_offset(len(ext_name)))
            colours = self._parse_colours(data,
                self._get_colours_offset(len(ext_name), len(short_name)))
            country = ''
            level = self._parse_level(data,
                self._get_level_offset(len(ext_name), len(short_name)))
            coach = ''
            players = []

            return Equipa(ext_name=ext_name, short_name=short_name,
                          country=country, level=level, colours=colours,
                          coach=coach, players=players)

    def _parse_ext_name(self, data):
        size = data[self.Offsets.HEADER_END.value + 1]
        data_offs = self.Offsets.HEADER_END.value + 2 # skip the 'size' byte

        return self._decrypt_field(data, data_offs, size)

    def _parse_short_name(self, data, offset):
        size = data[offset]

        return self._decrypt_field(data, offset + 1, size)

    def _parse_colours(self, data, offset):
        colours = [
            self._get_field(data, offset, self.Sizes.COLOUR.value).hex(),
            self._get_field(data, offset + self.Sizes.COLOUR.value + 1,
                            self.Sizes.COLOUR.value).hex()
        ]

        return colours

    def _parse_level(self, data, offset):
        level = self._get_field(data, offset, self.Sizes.LEVEL.value)

        return int(level.hex(), 16)

    def _get_field(self, data, offset, size):
        return data[offset:offset+size]

    def _decrypt_field(self, data, offset, size):
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
