from command.bulk_update import BulkUpdate
from event.update_equipa_listener import UpdateEquipaListener
from view.base_view import BaseView


class BulkUpdateView(BaseView, UpdateEquipaListener):

    def __init__(self, equipa_dir: str, provider: str, season: str):
        self._equipa_dir = equipa_dir
        self._prov = provider
        self._season = season

    def show(self) -> None:
        cmd = BulkUpdate(self._equipa_dir, self._prov, self._season, self)

        cmd.run()

    def on_update_equipa(self, equipa_name: str) -> None:
        pass

    def on_update_equipa_error(self, error: str) -> None:
        print(error)
