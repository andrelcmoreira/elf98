from typing import Optional

from libelifoot import (
    Equipa,
    UpdateEquipaListener
)


class EventHandler(UpdateEquipaListener):

    def __init__(self, dest):
        self._dest = dest

    def on_update_equipa(
        self,
        equipa_name: str,
        equipa_data: Optional[Equipa]
    ) -> None:
        self._dest.on_update_equipa(equipa_name, equipa_data)

    def on_update_equipa_error(self, error: str) -> None:
        self._dest.on_update_equipa_error(error)
