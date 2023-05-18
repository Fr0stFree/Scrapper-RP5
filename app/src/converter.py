from typing import Final

import geojson
import numpy as np
import pandas as pd

from .exceptions import ConvertingFailed


class CSVToFeatureConverter:
    DATETIME_COLUMN_NAME: Final[str] = 'datetime'

    def __init__(self, datetime_column: int, datetime_format: str) -> None:
        self._dt_column = datetime_column
        self._dt_format = datetime_format

    def df_to_collection(self, df: pd.DataFrame,
                         coordinates: tuple[float, float],
                         **extra_props: str) -> geojson.FeatureCollection:
        df = self._prepare_df(df)
        collection = self._convert_df_to_feature_collection(data=df, coordinates=coordinates, **extra_props)
        return collection

    def _prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df.replace(np.nan, None, inplace=True)
        df.rename(columns={df.columns[self._dt_column]: self.DATETIME_COLUMN_NAME}, inplace=True)
        df[self.DATETIME_COLUMN_NAME] = pd.to_datetime(df[self.DATETIME_COLUMN_NAME], format=self._dt_format)
        df[self.DATETIME_COLUMN_NAME] = df[self.DATETIME_COLUMN_NAME].apply(lambda x: x.isoformat())
        return df

    def _convert_df_to_feature_collection(self, data: pd.DataFrame,
                                          coordinates: tuple[float, float],
                                          **extra_props: str) -> geojson.FeatureCollection:
        collection = geojson.FeatureCollection([])
        for record in data.to_dict(orient='records'):
            record.update(extra_props)
            feature = geojson.Feature(geometry=geojson.Point(coordinates), properties=record)
            collection.features.append(feature)
        return collection
