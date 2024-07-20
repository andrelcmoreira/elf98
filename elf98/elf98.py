from sys import argv
from argparse import ArgumentParser

from command.factory import CommandFactory


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-v', '--view', action='store_true',
                        help="Print the equipa's data")
    parser.add_argument('-u', '--update', action='store_true',
                        help="Update an equipa specified by '-f' option")
    parser.add_argument('-b', '--bulk-update', action='store_true',
                        help='Update all the game equipas')
    parser.add_argument('-f', '--equipa-file', metavar='file',
                        help='Elifoot equipa file name')
    parser.add_argument('-p', '--provider', metavar='provider',
                        help='Team data provider')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main():
    args = parse_args()

    cmd = CommandFactory.create(args)
    if cmd:
        cmd.execute()


if __name__ == "__main__":
    main()
