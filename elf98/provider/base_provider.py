from abc import abstractmethod, ABC
from json import load

from util.player_position import PlayerPosition
from error.not_provided import EquipaNotProvided
from error.data_not_available import EquipaDataNotAvailable


class BaseProvider(ABC):

    def __init__(self, provider_name: str, base_url: str):
        self.name = provider_name
        self._base_url = base_url

    @abstractmethod
    def fetch_team_data(self, team_id: str) -> list | None:
        pass

    def get_team_id(self, equipa_file: str) -> str:
        with open(f'data/{self.name}.json', encoding='utf-8') as f:
            mapping = load(f)

            for entry in mapping:
                if entry['file'] == equipa_file:
                    return entry['id']

            return ''

    def get_teams(self) -> list:
        with open(f'data/{self.name}.json', encoding='utf-8') as f:
            mapping = load(f)

            return mapping

    def get_players(self, equipa_file: str) -> list:
        team_id = self.get_team_id(equipa_file)
        if team_id == '':
            raise EquipaNotProvided(equipa_file)

        players = self.fetch_team_data(team_id)
        if not players:
            raise EquipaDataNotAvailable(team_id)

        return self._select_players(players)

    def _select_players(self, player_list: list) -> list:
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

        # TODO: check the maximum number of players allowed by the game
        players.extend(gk[0:3])
        players.extend(df[0:6])
        players.extend(mf[0:6])
        players.extend(fw[0:6])

        return players
