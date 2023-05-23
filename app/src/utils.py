import sys
from pathlib import Path
from typing import Callable, Any

import geojson

from .settings import error_logger, base_logger


def save_geojson(data: geojson.GeoJSON, save_to: Path, name: str = 'result') -> None:
    with open(save_to / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))
        base_logger.info(f'GeoJSON saved to "{save_to}"')


def cleanup(path: Path) -> None:
    try:
        if path.is_dir():
            path.rmdir()
            base_logger.debug(f'Directory {path} has been deleted.')
        else:
            path.unlink()
            base_logger.debug(f'File {path} has been deleted.')

    except FileNotFoundError:
        error_logger.warning(f'File or dir on {path} does not exist.')


def log_errors(task: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        try:
            return task(*args, **kwargs)

        except Exception as exc:
            error_logger.error(str(exc))
            raise exc

    return inner
