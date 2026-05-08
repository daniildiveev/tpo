from __future__ import annotations

import os
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://x.com/"
LOGIN_URL = "https://x.com/i/flow/login"
HOME_URL = "https://x.com/home"
TIMEOUT = 10

USERNAME_INPUT = "//input[@autocomplete='username']"
PASSWORD_INPUT = "//input[@autocomplete='current-password']"
NEXT_BUTTON = "//button[.//span[normalize-space()='Next']]"
LOGIN_SUBMIT_BUTTON = "//button[@data-testid='LoginForm_Login_Button'] | //button[.//span[normalize-space()='Log in']]"

PRIMARY_COLUMN = "//div[@data-testid='primaryColumn']"
HOME_TIMELINE = "//div[@aria-label='Home timeline' or @data-testid='primaryColumn']"
FOR_YOU_TAB = "//*[@role='tab' and .//span[normalize-space()='For you']]"
FOLLOWING_TAB = "//*[@role='tab' and .//span[normalize-space()='Following']]"

TWEET_ARTICLE = "//article[@data-testid='tweet']"
TWEET_TEXT = ".//div[@data-testid='tweetText']"
TWEET_PERMALINK = ".//a[contains(@href, '/status/') and .//time]"
LIKE_BUTTON = ".//button[@data-testid='like']"
UNLIKE_BUTTON = ".//button[@data-testid='unlike']"

ACCOUNT_SWITCHER = "//div[@data-testid='SideNav_AccountSwitcher_Button']"
LOGOUT_MENU_ITEM = "//a[@data-testid='AccountSwitcher_Logout_Button'] | //div[@role='menuitem' and .//span[contains(normalize-space(), 'Log out')]]"
LOGOUT_CONFIRM = "//button[@data-testid='confirmationSheetConfirm']"

SEARCH_INPUT = "//input[@data-testid='SearchBox_Search_Input']"
SEARCH_RESULTS_TABLIST = "//div[@role='tablist']"
SEARCH_RESULTS_TAB_LATEST = "//*[@role='tab' and .//span[normalize-space()='Latest']]"
LOGOUT_URL = "https://x.com/logout"


def wait_present(driver: WebDriver, xpath: str, timeout: int = TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def wait_visible(driver: WebDriver, xpath: str, timeout: int = TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def click_xpath(driver: WebDriver, xpath: str) -> None:
    element = wait_present(driver, xpath)
    try:
        WebDriverWait(driver, TIMEOUT).until(
            lambda _: element.is_displayed() and element.is_enabled()
        )
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def element_exists(driver: WebDriver, xpath: str) -> bool:
    return bool(driver.find_elements(By.XPATH, xpath))


def perform_login(driver: WebDriver, username: str, password: str) -> None:
    driver.get(LOGIN_URL)
    user_field = wait_visible(driver, USERNAME_INPUT)
    time.sleep(1)
    user_field.send_keys(username)
    click_xpath(driver, NEXT_BUTTON)

    pwd_field = wait_visible(driver, PASSWORD_INPUT)
    time.sleep(1)
    pwd_field.send_keys(password)
    click_xpath(driver, LOGIN_SUBMIT_BUTTON)

    WebDriverWait(driver, TIMEOUT).until(
        lambda d: "/home" in d.current_url or element_exists(d, ACCOUNT_SWITCHER)
    )


def login_via_cookies(driver: WebDriver, cookies: dict) -> None:
    driver.get(BASE_URL)
    driver.delete_all_cookies()
    for name, value in cookies.items():
        driver.add_cookie(
            {
                "name": name,
                "value": value,
                "domain": ".x.com",
                "path": "/",
                "secure": True,
            }
        )
    driver.get(HOME_URL)
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: element_exists(d, ACCOUNT_SWITCHER) or element_exists(d, PRIMARY_COLUMN)
    )


@pytest.fixture
def authed_driver(driver: WebDriver) -> WebDriver:
    token = os.environ.get("X_AUTH_TOKEN")
    if token:
        cookies = {"auth_token": token}
        ct0 = os.environ.get("X_CT0")
        if ct0:
            cookies["ct0"] = ct0
        login_via_cookies(driver, cookies)
        return driver

    username = os.environ.get("X_USERNAME")
    password = os.environ.get("X_PASSWORD")
    if not username or not password:
        pytest.skip("Set X_AUTH_TOKEN or X_USERNAME/X_PASSWORD")
    perform_login(driver, username, password)
    return driver


# UC-07
@pytest.mark.xfail(
    reason="X anti-bot blocks Selenium-driven password login (Arkose/captcha). Use cookie auth.",
    strict=False,
)
def test_login_with_valid_credentials(driver: WebDriver, credentials: dict) -> None:
    perform_login(driver, credentials["username"], credentials["password"])

    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/home"))
    assert element_exists(driver, ACCOUNT_SWITCHER)
    assert element_exists(driver, PRIMARY_COLUMN)


# UC-08
def test_logout_returns_to_landing(authed_driver: WebDriver) -> None:
    authed_driver.get(LOGOUT_URL)
    confirm = wait_present(authed_driver, LOGOUT_CONFIRM, timeout=20)
    authed_driver.execute_script("arguments[0].click();", confirm)

    WebDriverWait(authed_driver, 20).until(
        lambda d: d.current_url.rstrip("/") in {BASE_URL.rstrip("/"), "https://x.com"}
        or "/i/flow/login" in d.current_url
        or "logout" in d.current_url
    )
    assert not element_exists(authed_driver, ACCOUNT_SWITCHER)
    assert not element_exists(authed_driver, PRIMARY_COLUMN) or "/i/flow/login" in authed_driver.current_url


# UC-09
def test_feed_shows_for_you_and_following_tabs(authed_driver: WebDriver) -> None:
    authed_driver.get(HOME_URL)

    wait_visible(authed_driver, PRIMARY_COLUMN)
    assert element_exists(authed_driver, FOR_YOU_TAB)
    assert element_exists(authed_driver, FOLLOWING_TAB)

    wait_present(authed_driver, TWEET_ARTICLE)
    initial = len(authed_driver.find_elements(By.XPATH, TWEET_ARTICLE))

    authed_driver.execute_script("window.scrollBy(0, 2000);")
    WebDriverWait(authed_driver, TIMEOUT).until(
        lambda d: len(d.find_elements(By.XPATH, TWEET_ARTICLE)) > initial
    )

    click_xpath(authed_driver, FOLLOWING_TAB)
    WebDriverWait(authed_driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, TWEET_ARTICLE))
    )


# UC-10
def test_open_individual_post(authed_driver: WebDriver) -> None:
    authed_driver.get(HOME_URL)

    article = wait_present(authed_driver, TWEET_ARTICLE)
    permalink = article.find_element(By.XPATH, TWEET_PERMALINK)
    href = permalink.get_attribute("href") or ""
    assert "/status/" in href
    try:
        permalink.click()
    except Exception:
        authed_driver.execute_script("arguments[0].click();", permalink)

    WebDriverWait(authed_driver, TIMEOUT).until(EC.url_contains("/status/"))
    assert "/status/" in authed_driver.current_url
    wait_present(authed_driver, "//article[@role='article']", timeout=20)
    assert element_exists(authed_driver, "//article[@role='article']")


# UC-11
def test_like_and_unlike_post(authed_driver: WebDriver) -> None:
    authed_driver.get(HOME_URL)

    article = wait_present(authed_driver, TWEET_ARTICLE)
    like_btn = WebDriverWait(authed_driver, TIMEOUT).until(
        lambda _: article.find_element(By.XPATH, LIKE_BUTTON)
    )
    authed_driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", like_btn
    )
    time.sleep(0.5)
    authed_driver.execute_script("arguments[0].click();", like_btn)

    WebDriverWait(authed_driver, TIMEOUT).until(
        lambda _: bool(article.find_elements(By.XPATH, UNLIKE_BUTTON))
    )
    assert article.find_elements(By.XPATH, UNLIKE_BUTTON)

    unlike_btn = article.find_element(By.XPATH, UNLIKE_BUTTON)
    authed_driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", unlike_btn
    )
    time.sleep(0.5)
    authed_driver.execute_script("arguments[0].click();", unlike_btn)

    WebDriverWait(authed_driver, TIMEOUT).until(
        lambda _: bool(article.find_elements(By.XPATH, LIKE_BUTTON))
    )
    assert article.find_elements(By.XPATH, LIKE_BUTTON)


# UC-12
def test_search_returns_results_page(authed_driver: WebDriver) -> None:
    authed_driver.get(HOME_URL)

    search_field = wait_visible(authed_driver, SEARCH_INPUT)
    search_field.click()
    query = "python"
    search_field.send_keys(query)
    time.sleep(1)
    search_field.send_keys(Keys.ENTER)

    WebDriverWait(authed_driver, TIMEOUT).until(EC.url_contains("/search"))
    assert "q=" in authed_driver.current_url
    wait_present(authed_driver, SEARCH_RESULTS_TABLIST, timeout=20)
    assert element_exists(authed_driver, SEARCH_RESULTS_TABLIST)

    if element_exists(authed_driver, SEARCH_RESULTS_TAB_LATEST):
        click_xpath(authed_driver, SEARCH_RESULTS_TAB_LATEST)

    wait_present(authed_driver, TWEET_ARTICLE, timeout=20)
    assert element_exists(authed_driver, TWEET_ARTICLE)
