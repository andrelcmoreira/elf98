from serializer.player import PlayerSerializer
from serializer.coach import CoachSerializer
from parser.equipa import EquipaParser
from util.offset import OffsetCalculator


class EquipaBuilder:

    @staticmethod
    def create_base_equipa(in_file, out_file):
        ep = EquipaParser(in_file)

        with open(in_file, 'r+b') as f:
            data = f.read()

            ext_name = ep.parse_ext_name(data)
            short_name = ep.parse_short_name(data, len(ext_name))
            offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

            out_file.write(data[:offs + 1])

    @staticmethod
    def add_players(file, players):
        for player in players:
            data = PlayerSerializer.serialize(player)

            file.write(data)

    @staticmethod
    def add_coach(file):
        data = CoachSerializer.serialize('Luis Zubeldia') # TODO: remove the hardcoded coach name

        file.write(data)

    @staticmethod
    def add_player_number(file, players_number):
        file.write(players_number.to_bytes())
