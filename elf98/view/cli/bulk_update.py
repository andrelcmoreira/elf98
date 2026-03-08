from typing import Optional

from libelifoot import (
    bulk_update,
    Equipa,
    EquipaFileHandler
)

from event.update_equipa import EventHandler
from view.base_view import BaseView


class BulkUpdate(BaseView):

    def __init__(
        self,
        equipa_dir: str,
        provider: str,
        season: int,
        output_directory: str
    ):
        self._equipa_dir = equipa_dir
        self._prov = provider
        self._season = season
        self._out_dir = output_directory
        self._ev = EventHandler(self)

    def show(self) -> None:
        bulk_update(self._equipa_dir, self._prov, self._season, self._ev)

    def on_update_equipa(
        self,
        equipa_name: str,
        equipa_data: Optional[Equipa]
    ) -> None:
        print(f'{equipa_name}\n{equipa_data}')

        if equipa_data:
            EquipaFileHandler.write(f'{equipa_name}.patch', equipa_data)

    def on_update_equipa_error(self, error: str) -> None:
        print(f'ERROR: {error}')
