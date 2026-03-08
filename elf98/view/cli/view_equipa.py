from libelifoot import get_equipa_data

from view.base_view import BaseView


class ViewEquipa(BaseView):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def show(self) -> None:
        equipa = get_equipa_data(self._equipa)

        print(equipa)
