from command.view import ViewEquipa
from view.base_view import BaseView
from entity.equipa import Equipa


class ShowEquipa(BaseView):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def show(self):
        cmd = ViewEquipa(self._equipa, self)

        cmd.run()

    def on_view_equipa(self, equipa_data: Equipa):
        print(equipa_data)

    def on_view_equipa_error(self, error: str):
        print(error)
