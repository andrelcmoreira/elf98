from command.command import Command
from command.update import UpdateEquipa
from event.update_equipa_listener import UpdateEquipaListener
from provider import provider_factory


class BulkUpdate(Command):

    def __init__(self, equipa_dir: str, provider: str, season: str,
                 output_directory: str, listener: UpdateEquipaListener):
        self._dir = equipa_dir
        self._prov = provider_factory.create(provider)
        self._season = season
        self._out_dir = output_directory
        self._listener = listener

    def run(self) -> None:
        teams = self._prov.get_teams()

        for team in teams:
            cmd = UpdateEquipa(self._dir + '/' + team['file'], self._prov.name,
                               self._season, self._out_dir, self._listener)

            cmd.run()
