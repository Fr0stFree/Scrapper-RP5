from unittest.mock import MagicMock, patch

import pytest

from app.src.extractor import StationCSVExtractor
from app.src.converter import CSVToFeatureConverter
from app.src import settings
from app.src import Station
from src.exceptions import ScenarioFailed


@pytest.fixture(scope='function')
def extractor():
    extractor = StationCSVExtractor()
    yield extractor
    del extractor


@pytest.fixture(scope='function')
def converter(extractor):
    converter = CSVToFeatureConverter(datetime_column=extractor.datetime_column,
                                      datetime_format=extractor.datetime_format)
    yield converter
    del converter


@pytest.fixture(scope='function')
def scenario(extractor):
    scenario = MagicMock()
    with patch('app.main.RP5ParseScenario', return_value=scenario):
        yield scenario
    del scenario


@pytest.fixture(scope='function')
def station_df(extractor):
    data_path = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'
    df = extractor.extract(data_path)
    yield df
    del df


@pytest.fixture(scope='function')
def station():
    station = Station(id='1250',
                      name='test_station',
                      url='https://test.url.ru',
                      latitude=12.50,
                      longitude=50.12)
    yield station
    del station
