from error.header_not_found import EquipaHeaderNotFound
from decoder.equipa import EquipaParser
from command.command import Command


class ViewEquipa(Command):

    def execute(self, **kwargs):
        equipa_file = kwargs.get('equipa_file')

        try:
            ep = EquipaParser(equipa_file)

            print(ep.parse())
        except EquipaHeaderNotFound as e:
            print(e)
