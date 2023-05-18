import geojson
import pytest
from unittest.mock import patch, Mock

from app.src import settings
from app.main import download_task
from app.src.exceptions import ScenarioFailed


class TestGetStationFeatureCollection:
    TEST_DATA_PATH = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'

    def test_will_fail_with_nonworkin_site(self, station, extractor, scenario, converter):
        scenario.download = Mock(side_effect=ScenarioFailed('Scenario Failed', url='https://rp5.ru/test'))

        with pytest.raises(ScenarioFailed) as excinfo:
            download_task(station, extractor, scenario, converter)

        assert scenario.download.called
        assert scenario.download.call_count == 1
        assert scenario.download.call_args.kwargs['url'] == station.url
        assert scenario.download.call_args.kwargs['save_to'] == settings.TEMP_DIR / station.id
        assert excinfo.value.url == 'https://rp5.ru/test'
        assert excinfo.value.message == 'Scenario Failed'

    def test_will_return_feature_collection(self, station, extractor, scenario, converter):
        scenario.download = Mock(return_value=self.TEST_DATA_PATH)
        with patch('app.main.cleanup', Mock()) as cleanup:

            result = download_task(station, extractor, scenario, converter)

            assert cleanup.called
            assert cleanup.call_count == 1
            assert cleanup.call_args[0][0] == self.TEST_DATA_PATH
            assert scenario.download.called
            assert scenario.download.call_count == 1
            assert isinstance(result, geojson.FeatureCollection)

            feature = result.features[0]

            assert feature.properties['id'] == station.id
            assert feature.properties['name'] == station.name
            assert feature.geometry.type == 'Point'
            assert feature.geometry.coordinates == [station.longitude, station.latitude]
