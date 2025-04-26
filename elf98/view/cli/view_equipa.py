from entity.equipa import Equipa
from event.view_equipa_listener import ViewEquipaListener
from view.base_view import BaseView

import command.view as command


class ViewEquipa(BaseView, ViewEquipaListener):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def show(self) -> None:
        cmd = command.ViewEquipa(self._equipa, self)

        cmd.run()

    def on_view_equipa(self, equipa_data: Equipa) -> None:
        print(equipa_data)

    def on_view_equipa_error(self, error: str) -> None:
        print(error)
