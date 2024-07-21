from util.sizes import Sizes
from util.offset import (Offsets, OffsetCalculator)
from util.crypto import decrypt
from parser.base_parser import BaseParser
from parser.player import PlayersParser
from entity.equipa import Equipa
from error.header_not_found import EquipaHeaderNotFound


class EquipaParser(BaseParser):

    def __init__(self, equipa_file):
        self._file = equipa_file

    def has_equipa_header(self, data):
        start_offs = Offsets.HEADER_START.value
        end_offs = Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def parse_ext_name(self, data):
        offs = OffsetCalculator.get_extended_name()
        size = data[Sizes.HEADER.value]

        return decrypt(data, offs, size)

    def parse_short_name(self, data, ext_len):
        offs = OffsetCalculator.get_short_name(ext_len)
        size = data[offs]

        return decrypt(data, offs + 1, size)

    def parse_colors(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_colors(ext_len, short_len)
        bg = self.get_field(data, offs, Sizes.COLOR.value)
        txt = self.get_field(data, offs + Sizes.COLOR.value + 1,
                             Sizes.COLOR.value)

        return '#' + bg.hex().upper() + ', #' + txt.hex().upper()

    def parse_level(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_level(ext_len, short_len)
        level = self.get_field(data, offs, Sizes.LEVEL.value)

        return int(level.hex(), 16)

    def parse_country(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_country(ext_len, short_len)

        return decrypt(data, offs, Sizes.COUNTRY.value)

    def parse_players(self, data, ext_len, short_len):
        players_offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        pp = PlayersParser(data, players_offs, count_offs)

        return pp.parse()

    def parse_coach(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_coach(data, ext_len, short_len)
        size = data[offs]

        return decrypt(data, offs + 1, size)

    def parse(self):
        with open(self._file, 'rb') as f:
            data = f.read()

            if not self.has_equipa_header(data):
                raise EquipaHeaderNotFound(self._file)

            ext_name = self.parse_ext_name(data)
            short_name = self.parse_short_name(data, len(ext_name))
            colors = self.parse_colors(data, len(ext_name), len(short_name))
            country = self.parse_country(data, len(ext_name), len(short_name))
            level = self.parse_level(data, len(ext_name), len(short_name))
            players = self.parse_players(data, len(ext_name), len(short_name))
            coach = self.parse_coach(data, len(ext_name), len(short_name))

            return Equipa(ext_name=ext_name, short_name=short_name,
                          country=country, level=level, colors=colors,
                          coach=coach, players=players)
