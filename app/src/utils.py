import sys
from pathlib import Path
from typing import Callable, Any

import geojson
import loguru

from . import exceptions, settings

logger = loguru.logger
logger.add(sink=settings.DATA_DIR / 'error.log', level='INFO', rotation='1 week')


def save_geojson(data: geojson.GeoJSON, save_to: Path, name: str = 'result') -> None:
    with open(save_to / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))
        logger.info(f'GeoJSON saved to "{save_to}"')


def cleanup(path: Path) -> None:
    try:
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()
    except FileNotFoundError:
        logger.warning(f'File or dir on {path} does not exist.')


def handle_errors(task: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        try:
            return task(*args, **kwargs)

        except exceptions.ScenarioFailed as exc:
            logger.error(f'Failed to parse page {exc.url}.\n'
                         f'An error occurred: {exc}')
            sys.exit(1)

        except exceptions.ConvertingFailed as exc:
            logger.error(f'Failed to convert dataframe.\n'
                         f'An error occurred: {exc}')
            sys.exit(1)

        except exceptions.InvalidStationCSV as exc:
            logger.error(f'Failed to parse station csv file {exc.path}.\n'
                         f'An error occurred: {exc}')

        except Exception as exc:
            logger.error(f'Unhandled exception: {exc}')
            sys.exit(1)

    return inner
