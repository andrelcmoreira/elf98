from os.path import exists

from command.command import Command
from error.header_not_found import EquipaHeaderNotFound
from error.not_found import EquipaNotFound
from parser.equipa import EquipaParser


class ViewEquipa(Command):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def run(self):
        if not exists(self._equipa):
            raise EquipaNotFound(self._equipa)

        try:
            ep = EquipaParser(self._equipa)

            print(ep.parse())
        except EquipaHeaderNotFound as e:
            print(e)
