from abc import ABC


class BaseClient(ABC):
    @property
    def data(self) -> dict:
        ...
