from pathlib import Path
from typing import Optional


class ScenarioFailed(Exception):
    def __init__(self, message: str, url: Optional[str] = None) -> None:
        super(ScenarioFailed, self).__init__(message)
        self.message = message
        self.url = url


class InvalidStationCSV(Exception):
    def __init__(self, message: str, path: Path) -> None:
        super(InvalidStationCSV, self).__init__(message)
        self.path = path

