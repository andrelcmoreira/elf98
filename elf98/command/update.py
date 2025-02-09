from os import mkdir
from os.path import sep, exists

from command.command import Command
from equipa.builder import EquipaBuilder
from error.data_not_available import EquipaDataNotAvailable
from error.not_found import EquipaNotFound
from error.not_provided import EquipaNotProvided
from event.update_equipa_listener import UpdateEquipaListener
from provider import provider_factory


class UpdateEquipa(Command):

    PATCH_PREFIX = 'PATCHED_'

    def __init__(self, equipa_file: str, provider: str, season: str,
                 output_directory: str, listener: UpdateEquipaListener):
        self._equipa = equipa_file
        self._prov = provider_factory.create(provider)
        self._season = season
        self._out_dir = output_directory
        self._listener = listener

    def run(self) -> None:
        equipa_file = self._equipa.split(sep)[-1]
        out_file = self.PATCH_PREFIX + equipa_file
        builder = EquipaBuilder()

        try:
            if not exists(self._out_dir):
                mkdir(self._out_dir)

            players = self._prov.get_players(equipa_file, self._season)

            with open(self._out_dir + '/' + out_file, 'wb') as f:
                # TODO: fill the coach name
                data = builder.create_base_equipa(self._equipa) \
                    .add_player_number(len(players)) \
                    .add_players(players) \
                    .add_coach('') \
                    .build()

                f.write(data)
                self._listener.on_update_equipa(self._equipa)
        except (EquipaNotProvided, EquipaDataNotAvailable, EquipaNotFound) as e:
            self._listener.on_update_equipa_error(e)
        except PermissionError as e:
            self._listener.on_update_equipa_error(e)
