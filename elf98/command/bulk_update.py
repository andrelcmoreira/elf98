from command.command import Command
from command.update import UpdateEquipa
from provider.factory import ProviderFactory
from error.unknown_provider import UnknownProvider


class BulkUpdate(Command):

    def __init__(self, provider, equipa_dir):
        self._prov = ProviderFactory.create(provider)
        self._dir = equipa_dir

        if not self._prov:
            raise UnknownProvider(provider)

    def run(self):
        teams = self._prov.get_teams()

        for team in teams:
            cmd = UpdateEquipa(self._dir + team['file'], self._prov.name)

            cmd.run()
