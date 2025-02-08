from command.command import Command
from command.update import UpdateEquipa
from event.bulk_update_listener import BulkUpdateEventListener
from provider import provider_factory


class BulkUpdate(Command):

    def __init__(self, equipa_dir: str, provider: str, season: str,
                 listener: BulkUpdateEventListener):
        self._dir = equipa_dir
        self._prov = provider_factory.create(provider)
        self._season = season
        self._listener = listener

    def run(self) -> None:
        teams = self._prov.get_teams()

        for team in teams:
            cmd = UpdateEquipa(self._dir + '/' + team['file'], self._prov.name,
                               self._season, self._listener)

            cmd.run()
