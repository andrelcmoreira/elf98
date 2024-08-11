from serializer.player import PlayerSerializer
from serializer.coach import CoachSerializer
from parser.equipa import EquipaParser
from util.offset import OffsetCalculator


class EquipaBuilder:

    def __init__(self, equipa_file):
        self._equipa = equipa_file
        self._data = bytearray()

    def create_base_equipa(self, in_file):
        ep = EquipaParser(in_file)

        with open(in_file, 'rb') as f:
            data = f.read()

            ext_name = ep.parse_ext_name(data)
            short_name = ep.parse_short_name(data, len(ext_name))
            offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

            self._data += data[:offs + 1]

        return self

    def add_players(self, players):
        for player in players:
            self._data += PlayerSerializer.serialize(player)

        return self

    def add_coach(self, coach):
        self._data += CoachSerializer.serialize(coach)

        return self

    def add_player_number(self, players_number):
        self._data += players_number.to_bytes()

        return self

    def build(self):
        return self._data
