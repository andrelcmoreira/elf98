from abc import ABC, abstractmethod


class BaseView(ABC):

    @abstractmethod
    def show(self):
        pass
