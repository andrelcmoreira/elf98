from os.path import exists, sep

from command.command import Command
from equipa.builder import EquipaBuilder
from error.data_not_available import EquipaDataNotAvailable
from error.not_found import EquipaNotFound
from error.not_provided import EquipaNotProvided
from provider.factory import ProviderFactory


class UpdateEquipa(Command):

    PATCH_PREFIX = 'PATCHED_'

    def __init__(self, equipa_file: str, provider: str, season: str):
        self._equipa = equipa_file
        self._prov = ProviderFactory.create(provider)
        self._season = season

    def run(self):
        if not exists(self._equipa):
            raise EquipaNotFound(self._equipa)

        equipa_file = self._equipa.split(sep)[-1]
        out_file = self.PATCH_PREFIX + equipa_file
        builder = EquipaBuilder()
        players = self._prov.get_players(equipa_file, self._season)

        with open(out_file, 'wb') as f:
            # TODO: fill the coach name
            data = builder.create_base_equipa(self._equipa) \
                .add_player_number(len(players)) \
                .add_players(players) \
                .add_coach('') \
                .build()

            f.write(data)
