from typing import Self


class Data:
    __data: dict
    
    def __init__(self):
        self.__data = {}

    def add(self, name: str, value) -> Self:
        self.__data[name] = value

        return self

    def get(self) -> dict:
        return self.__data
