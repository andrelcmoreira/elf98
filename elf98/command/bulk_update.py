from command.command import Command
from command.update import UpdateEquipa
from provider.factory import ProviderFactory
from view.base_view import BaseView


class BulkUpdate(Command):

    def __init__(self, equipa_dir: str, provider: str, season: str,
                 view: BaseView):
        self._dir = equipa_dir
        self._prov = ProviderFactory.create(provider)
        self._season = season
        self._view = view

    def run(self):
        teams = self._prov.get_teams()

        for team in teams:
            cmd = UpdateEquipa(self._dir + team['file'], self._prov.name,
                               self._season, self._view)

            cmd.run()
