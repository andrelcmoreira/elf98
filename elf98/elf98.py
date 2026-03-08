from argparse import ArgumentParser, Namespace
from typing import Optional

import sys
import os

from view import factory


#def run_gui():
#    from PyQt5.QtWidgets import QApplication
#    from elf98.main_window import MainWindow
#
#    app = QApplication(sys.argv)
#    window = MainWindow()
#    window.show()
#    sys.exit(app.exec_())


def parse_args() -> Optional[Namespace]:
    parser = ArgumentParser(prog=sys.argv[0],
                            description='Tool to view/patch elifoot98 equipas.')

    parser.add_argument('-b', '--bulk-update', metavar='equipas-directory',
                        help='update the equipas placed at the input directory')
    parser.add_argument('-u', '--update-equipa', metavar='equipa-file',
                        help="update an equipa")
    parser.add_argument('-v', '--view-equipa', metavar='equipa-file',
                        help="print the equipa data")
    parser.add_argument('-s', '--season-year', metavar='year', type=int,
                        help="the season's year to fetch the data")
    parser.add_argument('-p', '--provider', metavar='provider',
                        choices=['espn', 'transfermarkt'],
                        default='transfermarkt', help='team data provider')
    parser.add_argument('-o', '--output-directory', metavar='directory',
                        default=os.getcwd(),
                        help='output directory to put the patches on')

    # no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    view_instance = factory.create(args)
    view_instance.show()


if __name__ == "__main__":
    main()
