from abc import ABC, abstractmethod

from entity.equipa import Equipa


class ViewEquipaListener(ABC):

    @abstractmethod
    def on_view_equipa(self, equipa_data: Equipa) -> None:
        pass

    @abstractmethod
    def on_view_equipa_error(self, error: str) -> None:
        pass
