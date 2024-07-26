from os.path import sep

from command.command import Command
from provider.factory import ProviderFactory
from error.not_provided import EquipaNotProvided
from error.data_not_available import EquipaDataNotAvailable
from error.unknown_provider import UnknownProvider
from equipa.builder import EquipaBuilder


class UpdateEquipa(Command):

    def __init__(self, equipa_file, provider):
        self._equipa = equipa_file
        self._prov = ProviderFactory.create(provider)

        if not self._prov:
            raise UnknownProvider(provider)

    def run(self):
        equipa_file = self._equipa.split(sep)[-1]
        out_file = equipa_file + '.PATCHED'
        builder = EquipaBuilder(out_file)

        try:
            players = self._prov.get_players(equipa_file)

            with open(out_file, 'ab') as f:
                data = builder.create_base_equipa(self._equipa) \
                    .add_player_number(len(players)) \
                    .add_players(players) \
                    .add_coach() \
                    .build()

                f.write(data)
        except EquipaNotProvided as e:
            print(e)
        except EquipaDataNotAvailable as e:
            print(e)
