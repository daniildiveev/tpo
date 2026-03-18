from __future__ import annotations

from pathlib import Path

import pytest
from selenium import webdriver


CHROME_BINARY = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
FIREFOX_BINARY = Path("/Applications/Firefox.app/Contents/MacOS/firefox")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser for Selenium tests.",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode.",
    )


def _build_chrome(headed: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if CHROME_BINARY.exists():
        options.binary_location = str(CHROME_BINARY)
    if not headed:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 1400)
    driver.set_page_load_timeout(60)
    return driver


def _build_firefox(headed: bool) -> webdriver.Firefox:
    if not FIREFOX_BINARY.exists():
        pytest.skip("Firefox is not installed in the current environment.")

    options = webdriver.FirefoxOptions()
    options.binary_location = str(FIREFOX_BINARY)
    if not headed:
        options.add_argument("-headless")
    options.set_preference("intl.accept_languages", "en-US")
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1440, 1400)
    driver.set_page_load_timeout(60)
    return driver


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> webdriver.Remote:
    browser = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    if browser == "chrome":
        instance = _build_chrome(headed)
    else:
        instance = _build_firefox(headed)

    yield instance
    instance.quit()

