import datetime as dt
from pathlib import Path
from typing import Type
from typing_extensions import Self

from selenium.webdriver.common.by import By

from .webdriver.interface import DriverInterface, Locator
from .exceptions import ScenarioFailed
from .settings import base_logger


class RP5PageLocators:
    ARCHIVE_DOWNLOAD_TAB = Locator(By.ID, 'tabSynopDLoad')
    CSV_FORMAT_RADIO_BUTTON = Locator(By.XPATH, '//label[input/@id="format2"]/span')
    UTF8_ENCODING_RADIO_BUTTON = Locator(By.XPATH, '//label[input/@id="coding2"]/span')
    START_DATE_INPUT = Locator(By.ID, 'calender_dload')
    END_DATE_INPUT = Locator(By.ID, 'calender_dload2')
    REQUEST_ARCHIVE_BUTTON = Locator(By.CSS_SELECTOR, 'td.download > div.archButton')
    DOWNLOAD_ARCHIVE_BUTTON = Locator(By.CSS_SELECTOR, 'span#f_result > a')


class RP5ParseScenario:
    CALENDAR_DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, driver: Type[DriverInterface],
                 min_date: dt.date,
                 max_date: dt.date) -> None:
        self._Driver = driver
        self._min_date = min_date
        self._max_date = max_date
        self._driver_instance: DriverInterface | None = None

    def __enter__(self, *args, **kwargs) -> Self:
        try:
            self._driver_instance = self._Driver(*args, **kwargs)
            self._driver_instance.start()
            base_logger.info('Driver has been started.')
        except Exception as exc:
            raise ScenarioFailed(f'Unable to start webdriver: {self._Driver.__name__}.\n'
                                 f'An error occurred: {exc}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            self._driver_instance.finish()
            base_logger.info('Driver has been stopped.')
        except Exception as exc:
            raise ScenarioFailed(f'Unable to stop webdriver: {self._Driver.__name__}.\n'
                                 f'An error occurred: {exc}')

    def goto_page(self, url: str) -> Self:
        base_logger.debug(f'Opening "{url}"...')
        self._driver_instance.open(url)
        return self

    def goto_archive_tab(self) -> Self:
        base_logger.debug('Going to archive tab...')
        self._driver_instance.click(RP5PageLocators.ARCHIVE_DOWNLOAD_TAB)
        return self

    def select_csv_format(self) -> Self:
        base_logger.debug('Selecting csv format...')
        self._driver_instance.click(RP5PageLocators.CSV_FORMAT_RADIO_BUTTON)
        return self

    def select_utf8_encoding(self) -> Self:
        base_logger.debug('Selecting utf-8 encoding...')
        self._driver_instance.click(RP5PageLocators.UTF8_ENCODING_RADIO_BUTTON)
        return self

    def enter_min_calendar_date(self) -> Self:
        base_logger.debug(f'Setting up min calendar date to {self._min_date}...')
        self._driver_instance.input(RP5PageLocators.START_DATE_INPUT,
                                    value=self._min_date.strftime(self.CALENDAR_DATE_FORMAT))
        return self

    def enter_max_calendar_date(self) -> Self:
        base_logger.debug(f'Setting up max calendar date to {self._max_date}...')
        self._driver_instance.input(RP5PageLocators.START_DATE_INPUT,
                                    value=self._max_date.strftime(self.CALENDAR_DATE_FORMAT))
        return self

    def request_archive(self) -> Self:
        base_logger.debug('Requesting archive...')
        self._driver_instance.click(RP5PageLocators.REQUEST_ARCHIVE_BUTTON)
        return self

    def download_archive(self, save_to: Path) -> Self:
        base_logger.debug('Downloading archive...')
        self._driver_instance.download(RP5PageLocators.DOWNLOAD_ARCHIVE_BUTTON, save_to)
        return self

    def run(self, url: str, save_to: Path) -> Path:
        """Главная функция для вызова. Запускает процесс парсинга с одной страницы RP-5."""
        if not isinstance(self._driver_instance, DriverInterface):
            raise AttributeError('Driver has not been started.')

        try:
            self.goto_page(url) \
                .goto_archive_tab() \
                .select_csv_format() \
                .select_utf8_encoding() \
                .enter_min_calendar_date() \
                .enter_max_calendar_date() \
                .request_archive() \
                .download_archive(save_to)
            base_logger.info(f'Data from "{url}" has been parsed successfully')
            return save_to
        except Exception as exc:
            raise ScenarioFailed(f'Unable to parse page: {url}. An error occurred: {exc}', url)
