import geojson
import pandas as pd
import pytest

from app.src import settings
from app.src.converter import CSVToFeatureConverter
from app.src.exceptions import ConvertingFailed


class TestCSVToFeatureConverter:
    TEST_DATA_PATH = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'

    def test_convert_df_to_feature_collection(self, converter, station_df: pd.DataFrame) -> None:
        coordinates = [50.0, 20.0]
        extra_options = {'buzz': 23.5, 'foo': 'bar'}

        collection = converter.df_to_collection(station_df, coordinates, **extra_options)

        assert isinstance(collection, geojson.FeatureCollection)
        assert len(collection.features) == len(station_df)

        feature = collection.features[0]

        assert isinstance(feature, geojson.Feature)
        assert feature.geometry.type == 'Point'
        assert feature.geometry.coordinates == coordinates
        assert feature.properties['buzz'] == extra_options['buzz']
        assert feature.properties['foo'] == extra_options['foo']
        assert pd.to_datetime(feature.properties['datetime']).isoformat() == station_df['datetime'][0]
