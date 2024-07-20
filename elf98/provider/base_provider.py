from abc import abstractmethod, ABC
from json import load

from data.player_position import PlayerPosition


class BaseProvider(ABC):

    def __init__(self, provider_name, base_url):
        self._prov_name = provider_name
        self._base_url = base_url

    @abstractmethod
    def fetch_team_data(self, team_id):
        pass

    def get_team_id(self, equipa_file):
        with open(f'data/{self._prov_name}.json', encoding='utf-8') as f:
            mapping = load(f)

            for entry in mapping:
                if entry['file'] == equipa_file:
                    return entry['id']

            return ''

    def get_players(self, equipa_file):
        team_id = self.get_team_id(equipa_file)
        players = self.fetch_team_data(team_id)

        return self.select_players(players)

    def select_players(self, player_list):
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
