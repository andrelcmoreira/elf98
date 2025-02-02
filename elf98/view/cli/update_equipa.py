from command.update import UpdateEquipa
from event.update_equipa_listener import UpdateEquipaListener
from view.base_view import BaseView


class UpdateEquipaView(BaseView, UpdateEquipaListener):

    def __init__(self, equipa_file: str, provider: str, season: str):
        self._equipa = equipa_file
        self._prov = provider
        self._season = season

    def show(self) -> None:
        cmd = UpdateEquipa(self._equipa, self._prov, self._season, self)

        cmd.run()

    def on_update_equipa(self, equipa_name: str) -> None:
        pass

    def on_update_equipa_error(self, error: str) -> None:
        print(error)
