from command.view import ViewEquipa
from error.header_not_found import EquipaHeaderNotFound
from error.not_found import EquipaNotFound
from view.base_view import BaseView


class ShowEquipa(BaseView):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def show(self):
        try:
            cmd = ViewEquipa(self._equipa)

            print(cmd.run())
        except (EquipaHeaderNotFound, EquipaNotFound) as e:
            print(e)
