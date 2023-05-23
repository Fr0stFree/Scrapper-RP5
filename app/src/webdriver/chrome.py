from pathlib import Path
from typing import Self

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..settings import DEBUG
from .interface import DriverInterface, Locator


class ChromeDriver(DriverInterface):
    FAKE_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
    WAIT_LIMIT: int = 5  # sec

    def __init__(self) -> None:
        self._options = Options()
        self._options.headless = not DEBUG
        self._options.add_argument(f'User-Agent={self.FAKE_USER_AGENT}')
        self._options.add_argument("window-size=1920x1080")
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-dev-shm-usage')

    def start(self) -> Self:
        self._session = requests.session()
        self._session.headers = {'User-Agent': self.FAKE_USER_AGENT}
        self._chrome = webdriver.Chrome(options=self._options)
        return self

    def finish(self) -> None:
        self._session.close()
        self._chrome.close()

    def open(self, url: str) -> None:
        return self._chrome.get(url)

    def click(self, locator: Locator) -> None:
        self._wait_for_element(locator)
        self._chrome.find_element(*locator).click()

    def input(self, locator: Locator, value: str) -> None:
        self._wait_for_element(locator)
        element = self._chrome.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def download(self, locator: Locator, save_to: Path) -> None:
        self._wait_for_element(locator)
        url = self._chrome.find_element(*locator).get_attribute('href')
        response = self._session.get(url)
        with open(save_to, 'wb') as file:
            file.write(response.content)

    def _wait_for_element(self, locator: Locator) -> None:
        WebDriverWait(self._chrome, self.WAIT_LIMIT).until(EC.element_to_be_clickable(locator))
