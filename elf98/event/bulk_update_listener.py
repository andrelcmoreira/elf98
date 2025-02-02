from abc import ABC, abstractmethod


class BulkUpdateEventListener(ABC):

    @abstractmethod
    def on_update_equipa(self, equipa_name: str) -> None:
        pass

    @abstractmethod
    def on_update_equipa_error(self, error: str) -> None:
        pass
