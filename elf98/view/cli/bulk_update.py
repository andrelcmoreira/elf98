from event.update_equipa_listener import UpdateEquipaListener
from view.base_view import BaseView

import command.bulk_update as command


class BulkUpdate(BaseView, UpdateEquipaListener):

    def __init__(self, equipa_dir: str, provider: str, season: str,
                 output_directory: str):
        self._equipa_dir = equipa_dir
        self._prov = provider
        self._season = season
        self._out_dir = output_directory

    def show(self) -> None:
        cmd = command.BulkUpdate(self._equipa_dir, self._prov, self._season,
                                 self._out_dir, self)

        cmd.run()

    def on_update_equipa(self, equipa_name: str) -> None:
        pass

    def on_update_equipa_error(self, error: str) -> None:
        print(error)
