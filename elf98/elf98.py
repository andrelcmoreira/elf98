from sys import argv
from argparse import ArgumentParser

from command.factory import CommandFactory
from error.unknown_provider import UnknownProvider
from error.not_found import EquipaNotFound


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-v', '--view-equipa', action='store_true',
                        help="Print the equipa's data")
    parser.add_argument('-u', '--update-equipa', action='store_true',
                        help="Update an equipa specified by '-f' option")
    parser.add_argument('-b', '--bulk-update', action='store_true',
                        help='Update all the game equipas')
    parser.add_argument('-f', '--equipa-file', metavar='file',
                        required=True, help='Elifoot equipa file name')
    parser.add_argument('-p', '--provider', metavar='provider',
                        help='Team data provider')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        cmd = CommandFactory.create(args)
        if cmd:
            cmd.run()
    except UnknownProvider as e:
        print(e)
    except EquipaNotFound as e:
        print(e)


if __name__ == "__main__":
    main()