import pytest

from app.src.extractor import StationCSVExtractor
from app.src.converter import CSVToFeatureConverter
from app.src import settings


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
def station_df(extractor):
    data_path = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'
    df = extractor.extract(data_path)
    yield df
    del df
