from sys import argv
from argparse import ArgumentParser, Namespace

from command.factory import CommandFactory
from error.unknown_provider import UnknownProvider
from error.not_found import EquipaNotFound


def parse_args() -> Namespace | None:
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-b', '--bulk-update', action='store_true',
                        help='update all the game equipas')
    parser.add_argument('-d', '--equipas-dir', metavar='directory',
                        help="elifoot equipa's directory")
    parser.add_argument('-f', '--equipa-file', metavar='file',
                        help='elifoot equipa file name')
    parser.add_argument('-p', '--provider', metavar='provider',
                        choices=['espn'],
                        help='team data provider (currently only "espn" is \
                                supported)')
    parser.add_argument('-u', '--update-equipa', action='store_true',
                        help="update an equipa specified by '-f' option")
    parser.add_argument('-v', '--view-equipa', action='store_true',
                        help="print the equipa's data")

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
    except (UnknownProvider, EquipaNotFound) as e:
        print(e)


# TODO: improve error handling
# TODO: fetch coach name
# TODO: improve UI
# TODO: improve the code quality


if __name__ == "__main__":
    main()
