from command.command import Command
from command.update import UpdateEquipa
from event.update_equipa_listener import UpdateEquipaListener

import provider.factory


class BulkUpdate(Command):

    def __init__(self, equipa_dir: str, prov: str, season: str, output_dir: str,
                 listener: UpdateEquipaListener):
        self._dir = equipa_dir
        self._prov = provider.factory.create(prov)
        self._season = season
        self._out_dir = output_dir
        self._listener = listener

    def run(self) -> None:
        teams = self._prov.get_teams()

        for team in teams:
            cmd = UpdateEquipa(self._dir + '/' + team['file'], self._prov.name,
                               self._season, self._out_dir, self._listener)

            cmd.run()
