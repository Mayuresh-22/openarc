from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def handle(self, content: list[str]):
        raise NotImplementedError("Handle method must be implemented by subclasses")
