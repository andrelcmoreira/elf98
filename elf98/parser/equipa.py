from entity.equipa import Equipa
from error.header_not_found import EquipaHeaderNotFound
from error.not_found import EquipaNotFound
from parser.base_parser import BaseParser
from parser.player import PlayersParser
from util.crypto import decrypt
from util.offset import (Offsets, OffsetCalculator)
from util.sizes import Sizes


class EquipaParser(BaseParser):

    def __init__(self, equipa_file: str):
        self._file = equipa_file

    def has_equipa_header(self, data: bytes) -> bool:
        start_offs = Offsets.HEADER_START.value
        end_offs = Offsets.HEADER_END.value + 1

        return data[start_offs:end_offs] == b'EFa' + b'\x00' * 47

    def parse_ext_name(self, data: bytes) -> str:
        offs = OffsetCalculator.get_extended_name()
        size = data[Sizes.HEADER.value]

        return decrypt(data, offs, size)

    def parse_short_name(self, data: bytes, ext_len: int) -> str:
        offs = OffsetCalculator.get_short_name(ext_len)

        return decrypt(data, offs + 1, data[offs])

    def parse_colors(self, data: bytes, ext_len: int, short_len: int) -> str:
        offs = OffsetCalculator.get_colors(ext_len, short_len)
        bg = self.get_field(data, offs, Sizes.COLOR.value)
        txt = self.get_field(data, offs + Sizes.COLOR.value + 1,
                             Sizes.COLOR.value)

        return '#' + bg.hex().upper() + ', #' + txt.hex().upper()

    def parse_level(self, data: bytes, ext_len: int, short_len: int) -> int:
        offs = OffsetCalculator.get_level(ext_len, short_len)
        level = self.get_field(data, offs, Sizes.LEVEL.value)

        return int(level.hex(), 16)

    def parse_country(self, data: bytes, ext_len: int, short_len: int) -> str:
        offs = OffsetCalculator.get_country(ext_len, short_len)

        return decrypt(data, offs, Sizes.COUNTRY.value)

    def parse_players(self, data: bytes, ext_len: int, short_len: int) -> list:
        players_offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        pp = PlayersParser(data, players_offs, count_offs)

        return pp.parse()

    def parse_coach(self, data: bytes, ext_len: int, short_len: int) -> str:
        offs = OffsetCalculator.get_coach(data, ext_len, short_len)
        if offs > len(data): # no coach information available
            return ''

        return decrypt(data, offs + 1, data[offs])

    def parse(self) -> Equipa:
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
