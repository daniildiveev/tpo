from __future__ import annotations

import os
from pathlib import Path

import pytest
from selenium import webdriver


def _load_env_file() -> None:
    candidates = [
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    for path in candidates:
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


_load_env_file()


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


@pytest.fixture
def credentials() -> dict[str, str]:
    username = os.environ.get("X_USERNAME")
    password = os.environ.get("X_PASSWORD")
    if not username or not password:
        pytest.skip("X_USERNAME / X_PASSWORD not set in environment or .env")
    return {"username": username, "password": password}


@pytest.fixture
def auth_cookies() -> dict[str, str]:
    token = os.environ.get("X_AUTH_TOKEN")
    if not token:
        pytest.skip("X_AUTH_TOKEN not set in environment or .env")
    cookies = {"auth_token": token}
    ct0 = os.environ.get("X_CT0")
    if ct0:
        cookies["ct0"] = ct0
    return cookies

