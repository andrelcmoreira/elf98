from json import loads
from os.path import sep

from command.command import Command
from data.player_position import PlayerPosition
from decoder.equipa import EquipaParser
from decoder.equipa import OffsetCalculator
from encoder.serializer import Serializer
from entity.player import Player
from provider.factory import ProviderFactory
from error.not_provided import EquipaNotProvided
from error.data_not_available import EquipaDataNotAvailable


class UpdateEquipa(Command):

    def __init__(self, equipa_file, provider):
        self._equipa = equipa_file
        self._prov = ProviderFactory.create(provider)

    def run(self):
        equipa_file = self._equipa.split(sep)[-1]
        out_file = equipa_file + '.PATCHED'

        try:
            players = self._prov.get_players(equipa_file)

            with open(out_file, 'ab') as f:
                self._create_base_equipa(self._equipa, f)
                self._add_player_number(f, len(players))
                self._add_players(f, players)
                self._add_coach(f)
        except EquipaNotProvided as e:
            print(e)
        except EquipaDataNotAvailable as e:
            print(e)

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

    def _add_player_number(self, file, players_number):
        file.write(players_number.to_bytes())

    def _create_base_equipa(self, in_file, out_file):
        ep = EquipaParser(in_file)

        with open(in_file, 'r+b') as f:
            data = f.read()

            ext_name = ep.parse_ext_name(data)
            short_name = ep.parse_short_name(data, len(ext_name))
            offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

            out_file.write(data[:offs + 1])
