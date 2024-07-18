from sys import argv
from dataclasses import dataclass
from enum import Enum
from json import loads
from re import findall

from argparse import ArgumentParser
from requests import get
from unidecode import unidecode


class Offsets(Enum):
    HEADER_START = 0x00
    HEADER_END = 0x31


class Sizes(Enum):
    HEADER = 50
    COLOR = 3 # each color has 3 bytes
    LEVEL = 1
    COUNTRY = 4 # encrypted size
    EQUIPA_SIZE = 1


class PlayerPosition(Enum):
    G = 0
    D = 1
    M = 2
    A = 3 # forward ('atacante' in portuguese)


@dataclass
class Player:

    name: str
    position: str
    country: str
    appearances: int

    def __repr__(self):
        return f'{self.position}: {self.name} - {self.country}'


class OffsetCalculator:

    @staticmethod
    def get_extended_name():
        # +1 to skip the size byte
        return Sizes.HEADER.value + 1

    @staticmethod
    def get_short_name(ext_len):
        # +1 to skip the size byte of extended name field
        return Sizes.HEADER.value + ext_len + 1

    @staticmethod
    def get_colors(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        return Sizes.HEADER.value + ext_len + short_len + 2

    @staticmethod
    def get_country(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + 4

    @staticmethod
    def get_level(ext_len, short_len):
        # +1 to skip the size byte of extended field
        # +1 to skip the size byte of short name field
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + 4

    @staticmethod
    def get_players_number(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each color
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + \
            Sizes.LEVEL.value + 4

    @staticmethod
    def get_players(ext_len, short_len):
        # +2 to skip the size bytes of extended and short name fields
        # +2 to skip the apparently unused 1 byte on each color
        # +1 to skip to the player nationality
        return Sizes.HEADER.value + ext_len + short_len + \
            Sizes.COLOR.value * 2 + Sizes.COUNTRY.value + \
            Sizes.LEVEL.value + Sizes.EQUIPA_SIZE.value + 5

    @staticmethod
    def get_coach(data, ext_len, short_len):
        offs = OffsetCalculator.get_players(ext_len, short_len)
        count_offs = OffsetCalculator.get_players_number(ext_len, short_len)
        number_players = data[count_offs]

        for _ in range(0, number_players):
            entry_len = data[offs + Sizes.COUNTRY.value]
            # +1 to skip the 'name size' byte
            # +1 to skip the position byte
            # +1 to jump to the next entry
            offs += Sizes.COUNTRY.value + entry_len + 3

        return offs


class EquipaParser:

    def __init__(self, equipa_file):
        self._file = equipa_file

    @staticmethod
    def parse_ext_name(data):
        offs = OffsetCalculator.get_extended_name()
        size = data[Sizes.HEADER.value]

        return decrypt(data, offs, size)

    @staticmethod
    def parse_short_name(data, ext_len):
        offs = OffsetCalculator.get_short_name(ext_len)
        size = data[offs]

        return decrypt(data, offs + 1, size)


def decrypt(data, offset, size):
    ret = ''

    for i in range(offset, offset + size):
        ret += chr((data[i] - data[i - 1]) & 0xff)

    return ret


def to_pos_code(pos):
    match pos:
        case PlayerPosition.G.name: return PlayerPosition.G.value
        case PlayerPosition.D.name: return PlayerPosition.D.value
        case PlayerPosition.M.name: return PlayerPosition.M.value
        case PlayerPosition.A.name: return PlayerPosition.A.value


def encrypt(text):
    out = bytearray()

    out.append(len(text))
    for i in range(0, len(text)):
        out.append((ord(text[i]) + out[i]) & 0xff)

    return out


def add_players(file, players):
    player = bytearray()

    for entry in players:
        player.append(0)
        player += encrypt(entry.country)
        player += encrypt(entry.name)
        player.append(to_pos_code(entry.position))

        file.write(player)
        player.clear()


def add_coach(file):
    coach = bytearray()

    coach.append(0)
    coach += encrypt('Luis Zubeldia') # TODO: remove the hardcoded coach name

    file.write(coach)


def add_player_number(file, players):
    file.write(len(players).to_bytes())


def create_base_equipa(in_file, out_file):
    with open(in_file, 'r+b') as f:
        data = f.read()

        ext_name = EquipaParser.parse_ext_name(data)
        short_name = EquipaParser.parse_short_name(data, len(ext_name))
        offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

        out_file.write(data[:offs + 1])


def update_equipa(in_file, espn_id, out_file):
    players = fetch_team_data(espn_id)

    if not players:
        return

    with open(out_file, 'ab') as f:
        create_base_equipa(in_file, f)
        add_player_number(f, players)
        add_players(f, players)
        add_coach(f)


def fetch_team_data(espn_id):
    base_url = 'https://www.espn.com.br/futebol/time/elenco/_/id/'
    headers = { 'User-Agent': 'elf98' }
    reply = get(base_url + espn_id, headers=headers, timeout=5)

    ret = findall(r'(\"athletes\":[\[\{"\w:,\/\.\d~\-\s\}\\p{L}]+\])',
                  reply.text)

    try:
        goalkeepers = loads('{' + ret[0] + '}')
        others = loads('{' + ret[1] + '}')

        return parse_players(goalkeepers, others)
    except IndexError:
        return None


def get_country(country):
    cnt = country[0:3].upper()

    match cnt:
        case 'VEN': return 'VNZ'
        case 'REP': return 'RCH'

    return unidecode(cnt)


def parse_players(goalkeepers, others):
    players = []

    for player in goalkeepers['athletes']:
        players.append(
            Player(
                name=player['name'],
                position=player['position'],
                country=get_country(player['ctz']),
                appearances=player.get('appearances') \
                    if player.get('appearances') is not None \
                    else 0
            )
        )

    for player in others['athletes']:
        players.append(
            Player(
                name=player['name'],
                position=player['position'],
                country=get_country(player['ctz']),
                appearances=player.get('appearances') \
                    if player.get('appearances') is not None \
                    else 0
            )
        )

    return select_players(players)


def select_players(player_list):
    players = []
    gk = []
    df = []
    mf = []
    fw = []

    for player in player_list:
        match player.position:
            case PlayerPosition.G.name: gk.append(player)
            case PlayerPosition.D.name: df.append(player)
            case PlayerPosition.M.name: mf.append(player)
            case PlayerPosition.A.name: fw.append(player)

    gk.sort(key=lambda p: int(p.appearances), reverse=True)
    df.sort(key=lambda p: int(p.appearances), reverse=True)
    mf.sort(key=lambda p: int(p.appearances), reverse=True)
    fw.sort(key=lambda p: int(p.appearances), reverse=True)

    players.extend(gk[0:3])
    players.extend(df[0:6])
    players.extend(mf[0:6])
    players.extend(fw[0:6])

    return players


def main():
    args = parse_args()

    if args:
        update_equipa(args.equipa_file,
                      args.espn_id,
                      args.output_file)


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-e', '--equipa-file', metavar='file',
                        help='Elifoot equipa file name')
    parser.add_argument('-i', '--espn-id', metavar='ID',
                        help='Team ID (extracted from ESPN site)')
    parser.add_argument('-o', '--output-file', metavar='file',
                        help='Output file name')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


# TODO: remove duplicated code
# TODO: test the regex with more teams
if __name__ == "__main__":
    main()
