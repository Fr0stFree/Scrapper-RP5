import datetime as dt
from typing_extensions import Annotated
import geojson
import typer

from src import Station, stations, settings
from src.converter import CSVToFeatureConverter
from src.webdriver import ChromeDriver
from src.scenario import RP5ParseScenario
from src.extractor import StationCSVExtractor
from src.utils import save_geojson, cleanup, handle_errors


def main(
        min_date: Annotated[dt.datetime, typer.Argument(
            help='Date from which to start downloading data'
        )] = dt.datetime.now() - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS),
        max_date: Annotated[dt.datetime, typer.Argument(
            help='Date to which to download data'
        )] = dt.datetime.now(),
) -> None:
    data = geojson.FeatureCollection([])

    with RP5ParseScenario(ChromeDriver, min_date, max_date) as downloader:
        extractor = StationCSVExtractor()
        converter = CSVToFeatureConverter(datetime_column=extractor.datetime_column,
                                          datetime_format=extractor.datetime_format)
        for station in stations:
            collection = handle_errors(download_task)(station, extractor, downloader, converter)
            data.update(collection)

    save_geojson(data, save_to=settings.DATA_DIR)
    cleanup(settings.TEMP_DIR)


def download_task(station: Station,
                  extractor: StationCSVExtractor,
                  downloader: RP5ParseScenario,
                  converter: CSVToFeatureConverter) -> geojson.FeatureCollection:
    file_path = downloader.download(url=station.url, save_to=settings.TEMP_DIR / station.id)
    df = extractor.extract(file_path)
    extra_props = {'id': station.id, 'name': station.name}
    feature_collection = converter.df_to_collection(df, coordinates=(station.longitude, station.latitude),
                                                    **extra_props)

    cleanup(file_path)
    return feature_collection


if __name__ == '__main__':
    typer.run(main)
