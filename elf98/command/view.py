from error.header_not_found import EquipaHeaderNotFound
from parser.equipa import EquipaParser
from command.command import Command


class ViewEquipa(Command):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def run(self):
        try:
            ep = EquipaParser(self._equipa)

            print(ep.parse())
        except EquipaHeaderNotFound as e:
            print(e)
