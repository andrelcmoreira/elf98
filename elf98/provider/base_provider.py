from abc import abstractmethod, ABC
from json import load
from requests import exceptions, get
from unidecode import unidecode

from error.data_not_available import EquipaDataNotAvailable
from error.not_provided import EquipaNotProvided


class BaseProvider(ABC):

    _REQUEST_TIMEOUT = 10
    _MAX_GK_PLAYERS = 3
    _MAX_DEF_PLAYERS = 6
    _MAX_MD_PLAYERS = 6
    _MAX_FW_PLAYERS = 6
    _MAX_NAME_SIZE = 18

    def __init__(self, provider_name: str, base_url: str, country_map: dict):
        self._name = provider_name
        self._base_url = base_url
        self._country_map = country_map

    @abstractmethod
    def assemble_uri(self, team_id: str, season: str) -> str:
        pass

    @abstractmethod
    def parse_reply(self, reply: str) -> list | None:
        pass

    @abstractmethod
    def select_players(self, player_list: list) -> list:
        pass

    @property
    def name(self) -> str:
        return self._name

    def get_country(self, country: str) -> str:
        return self._country_map[country] \
            if country in self._country_map \
            else unidecode(country[0:3]).upper()

    def fetch_team_data(self, team_id: str, season: str) -> list | None:
        headers = { 'User-Agent': 'elf98' }
        uri = self.assemble_uri(team_id, season)

        try:
            reply = get(uri, headers=headers, timeout=self._REQUEST_TIMEOUT)

            return self.parse_reply(reply)
        except exceptions.ConnectionError:
            return None

    def get_team_id(self, equipa_file: str) -> str:
        with open(f'data/{self._name}.json', encoding='utf-8') as f:
            mapping = load(f)

            for entry in mapping:
                if entry['file'] == equipa_file:
                    return entry['id']

            return ''

    def get_teams(self) -> list:
        with open(f'data/{self._name}.json', encoding='utf-8') as f:
            mapping = load(f)

            return mapping

    def get_players(self, equipa_file: str, season: str) -> list:
        team_id = self.get_team_id(equipa_file)
        if team_id == '':
            raise EquipaNotProvided(equipa_file)

        players = self.fetch_team_data(team_id, season)
        if not players:
            raise EquipaDataNotAvailable(equipa_file)

        return self.select_players(players)
