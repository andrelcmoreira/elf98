from json import loads
from re import findall
from requests import get
from unidecode import unidecode

from command.command import Command
from data.player_position import PlayerPosition
from decoder.equipa import EquipaParser
from decoder.equipa import OffsetCalculator
from encoder.serializer import Serializer
from entity.player import Player


class UpdateEquipa(Command):

    def execute(self, **kwargs):
        equipa_file = kwargs.get('equipa_file')
        out_file = equipa_file + '.PATCHED'
        players = self._fetch_team_data(kwargs.get('espn_id'))

        print(equipa_file)

        if not players:
            return

        with open(out_file, 'ab') as f:
            self._create_base_equipa(equipa_file, f)
            self._add_player_number(f, players)
            self._add_players(f, players)
            self._add_coach(f)

    def _get_country(self, country):
        cnt = country[0:3].upper()

        match cnt:
            case 'VEN': return 'VNZ'
            case 'REP': return 'RCH'

        return unidecode(cnt)

    def _fetch_team_data(self, espn_id):
        base_url = 'https://www.espn.com.br/futebol/time/elenco/_/id/'
        headers = { 'User-Agent': 'elf98' }
        reply = get(base_url + espn_id, headers=headers, timeout=5)

        ret = findall(r'(\"athletes\":[\[\{"\w:,\/\.\d~\-\s\}\\p{L}]+\])',
                      reply.text)

        try:
            goalkeepers = loads('{' + ret[0] + '}')
            others = loads('{' + ret[1] + '}')

            return self._parse_players(goalkeepers, others)
        except IndexError:
            return None

    def _parse_players(self, goalkeepers, others):
        players = []

        for player in goalkeepers['athletes']:
            players.append(
                Player(
                    name=player['name'],
                    position=player['position'],
                    country=self._get_country(player['ctz']),
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
                    country=self._get_country(player['ctz']),
                    appearances=player.get('appearances') \
                        if player.get('appearances') is not None \
                        else 0
                )
            )

        return self._select_players(players)

    def _select_players(self, player_list):
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

    def _to_pos_code(self, pos):
        match pos:
            case PlayerPosition.G.name: return PlayerPosition.G.value
            case PlayerPosition.D.name: return PlayerPosition.D.value
            case PlayerPosition.M.name: return PlayerPosition.M.value
            case PlayerPosition.A.name: return PlayerPosition.A.value

    def _add_players(self, file, players):
        player = bytearray()

        for entry in players:
            player.append(0)
            player += Serializer.encrypt(entry.country)
            player += Serializer.encrypt(entry.name)
            player.append(self._to_pos_code(entry.position))

            file.write(player)
            player.clear()

    def _add_coach(self, file):
        coach = bytearray()

        coach.append(0)
        coach += Serializer.encrypt('Luis Zubeldia') # TODO: remove the hardcoded coach name

        file.write(coach)


    def _add_player_number(self, file, players):
        file.write(len(players).to_bytes())


    def _create_base_equipa(self, in_file, out_file):
        ep = EquipaParser(in_file)

        with open(in_file, 'r+b') as f:
            data = f.read()

            ext_name = ep.parse_ext_name(data)
            short_name = ep.parse_short_name(data, len(ext_name))
            offs = OffsetCalculator.get_level(len(ext_name), len(short_name))

            out_file.write(data[:offs + 1])
