from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self, NamedTuple


class Locator(NamedTuple):
    by: str
    value: str


class DriverInterface(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def start(self) -> Self:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass

    @abstractmethod
    def open(self, url: str) -> None:
        """Приказывает драйверу перейти по указанной ссылке"""
        pass

    @abstractmethod
    def click(self, locator: Locator) -> None:
        """Приказывает драйверу найти элемент на странице и нажать на него"""
        pass

    @abstractmethod
    def input(self, locator: Locator, value: str) -> None:
        """Приказывает драйверу найти поле на странице и ввести в него строку"""
        pass

    @abstractmethod
    def download(self, locator: Locator, save_to: Path) -> None:
        """Приказывает драйверу скачать файл по указанной ссылке в элементе"""
        pass


