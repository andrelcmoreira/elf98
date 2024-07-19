from sys import argv

from error.header_not_found import EquipaHeaderNotFound
from decoder.equipa import (EquipaParser)


def main(equipa_file):
    try:
        ep = EquipaParser(equipa_file)

        print(ep.parse())
    except EquipaHeaderNotFound as e:
        print(e)


if __name__ == "__main__":
    if len(argv) == 2:
        main(argv[1])
    else:
        print(f'usage: {argv[0]} <equipa_file>')
