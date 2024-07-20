from json import loads
from os.path import sep

from command.command import Command
from data.player_position import PlayerPosition
from decoder.equipa import EquipaParser
from decoder.equipa import OffsetCalculator
from encoder.serializer import Serializer
from entity.player import Player
from provider.factory import ProviderFactory


class UpdateEquipa(Command):

    def __init__(self, equipa_file, provider):
        self._equipa = equipa_file
        self._prov = ProviderFactory.create(provider)

    def execute(self):
        equipa_file = self._equipa.split(sep)[-1]
        out_file = equipa_file + '.PATCHED'
        team_id = self._prov.get_team_id(equipa_file)
        players = self._prov.fetch_team_data(team_id)

        if not players:
            return

        with open(out_file, 'ab') as f:
            self._create_base_equipa(self._equipa, f)
            self._add_player_number(f, players)
            self._add_players(f, players)
            self._add_coach(f)

    def _add_players(self, file, players):
        player = bytearray()

        for entry in players:
            player.append(0)
            player += Serializer.encrypt(entry.country)
            player += Serializer.encrypt(entry.name)
            player.append(self._to_pos_code(entry.position))

            file.write(player)
            player.clear()

    def _to_pos_code(self, pos):
        match pos:
            case PlayerPosition.G.name: return PlayerPosition.G.value
            case PlayerPosition.D.name: return PlayerPosition.D.value
            case PlayerPosition.M.name: return PlayerPosition.M.value
            case PlayerPosition.A.name: return PlayerPosition.A.value

    def _add_coach(self, file):
        coach = bytearray()

        coach.append(0)
        coach += Serializer.encrypt('Luis Zubeldia') # TODO: remove the hardcoded coach name

        file.write(coach)

    def _add_player_number(self, file, players):
        file.write(len(players).to_bytes())

    def _create_base_equipa(self, in_file, out_file):
        ep = EquipaParser(in_file)

        with open(in_file, 'r+b') as f:
            data = f.read()

            ext_name = ep.parse_ext_name(data)
            short_name = ep.parse_short_name(data, len(ext_name))
            offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

            out_file.write(data[:offs + 1])
