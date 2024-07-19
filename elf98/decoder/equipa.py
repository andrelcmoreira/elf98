from data.sizes import Sizes
from data.offsets import Offsets
from decoder.base import BaseParser
from decoder.player import PlayersParser
from entity.equipa import Equipa
from error.header_not_found import EquipaHeaderNotFound


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

        return self.decrypt_field(data, offs, size)

    def parse_short_name(self, data, ext_len):
        offs = OffsetCalculator.get_short_name(ext_len)
        size = data[offs]

        return self.decrypt_field(data, offs + 1, size)

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

        return self.decrypt_field(data, offs, Sizes.COUNTRY.value)

    def parse_players(self, data, ext_len, short_len):
        players_offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        pp = PlayersParser(data, players_offs, count_offs)

        return pp.parse()

    def parse_coach(self, data, ext_len, short_len):
        offs = OffsetCalculator.get_coach(data, ext_len, short_len)
        size = data[offs]

        return self.decrypt_field(data, offs + 1, size)

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
