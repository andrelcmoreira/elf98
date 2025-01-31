from command.command import Command
from error.not_found import EquipaNotFound
from parser.equipa import EquipaParser
from view.base_view import BaseView
from error.header_not_found import EquipaHeaderNotFound
from error.not_found import EquipaNotFound


class ViewEquipa(Command):

    def __init__(self, equipa_file: str, view: BaseView):
        self._equipa = equipa_file
        self._view = view

    def run(self) -> str:
        try:
            ep = EquipaParser(self._equipa)

            self._view.on_view_equipa(ep.parse())
        except (EquipaHeaderNotFound, EquipaNotFound, EquipaNotFound) as e:
            self._view.on_view_equipa_error(e)
