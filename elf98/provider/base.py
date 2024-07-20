from abc import abstractmethod, ABC

from data.player_position import PlayerPosition


class Base(ABC):

    @abstractmethod
    def fetch_team_data(self, team_id):
        pass

    @abstractmethod
    def parse_mapping(self):
        pass

    @abstractmethod
    def get_team_id(self, equipa_file):
        pass

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
