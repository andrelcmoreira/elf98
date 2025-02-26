from os import getcwd
from sys import argv
from argparse import ArgumentParser, Namespace

from view import view_factory


def parse_args() -> Namespace | None:
    parser = ArgumentParser(prog=argv[0],
                            description='Tool to view/patch elifoot98 equipas.')

    parser.add_argument('-b', '--bulk-update', metavar='equipas-directory',
                        help='update the equipas placed at the input directory')
    parser.add_argument('-u', '--update-equipa', metavar='equipa-file',
                        help="update an equipa")
    parser.add_argument('-v', '--view-equipa', metavar='equipa-file',
                        help="print the equipa data")
    parser.add_argument('-s', '--season', metavar='year', default='',
                        help="the season's year to fetch the data")
    parser.add_argument('-p', '--provider', metavar='provider',
                        choices=['espn'], default='espn',
                        help='team data provider (currently only "espn" is \
                                supported)')
    parser.add_argument('-o', '--output-directory', metavar='directory',
                        default=getcwd(),
                        help='output directory to put the patches on')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args:
        return

    view = view_factory.create(args)
    if view:
        view.show()


# TODO: improve error handling
# TODO: improve the code quality


if __name__ == "__main__":
    main()
