from sys import argv
from json import loads
from re import findall

from argparse import ArgumentParser
from requests import get
from unidecode import unidecode

from data.offsets import Offsets
from data.sizes import Sizes
from data.player_position import PlayerPosition
from decoder.player import PlayersParser
from decoder.equipa import (EquipaParser, OffsetCalculator)
from entity.player import Player
from encoder.serializer import Serializer


def to_pos_code(pos):
    match pos:
        case PlayerPosition.G.name: return PlayerPosition.G.value
        case PlayerPosition.D.name: return PlayerPosition.D.value
        case PlayerPosition.M.name: return PlayerPosition.M.value
        case PlayerPosition.A.name: return PlayerPosition.A.value


def add_players(file, players):
    player = bytearray()

    for entry in players:
        player.append(0)
        player += Serializer.encrypt(entry.country)
        player += Serializer.encrypt(entry.name)
        player.append(to_pos_code(entry.position))

        file.write(player)
        player.clear()


def add_coach(file):
    coach = bytearray()

    coach.append(0)
    coach += Serializer.encrypt('Luis Zubeldia') # TODO: remove the hardcoded coach name

    file.write(coach)


def add_player_number(file, players):
    file.write(len(players).to_bytes())


def create_base_equipa(in_file, out_file):
    ep = EquipaParser(in_file)

    with open(in_file, 'r+b') as f:
        data = f.read()

        ext_name = ep.parse_ext_name(data)
        short_name = ep.parse_short_name(data, len(ext_name))
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
# TODO: gui interface?
if __name__ == "__main__":
    main()
