from os.path import exists

from command.command import Command
from error.not_found import EquipaNotFound
from parser.equipa import EquipaParser


class ViewEquipa(Command):

    def __init__(self, equipa_file: str):
        self._equipa = equipa_file

    def run(self) -> str:
        if not exists(self._equipa):
            raise EquipaNotFound(self._equipa)

        ep = EquipaParser(self._equipa)

        return ep.parse()
