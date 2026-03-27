from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://x.com/"
LOGIN_URL = "https://x.com/i/flow/login"
TIMEOUT = 45

COOKIE_REFUSE_BUTTON = "//button[.//span[normalize-space()='Refuse non-essential cookies']]"
HAPPENING_NOW_HEADING = "//*[self::h1 or self::span][normalize-space()='Happening now']"
CREATE_ACCOUNT_LINK = "//a[@role='link' and .//span[normalize-space()='Create account']]"
SIGN_IN_LINK = "//a[@role='link' and .//span[normalize-space()='Sign in']]"
TERMS_OF_SERVICE_LINK = "//a[@role='link' and contains(@href, 'tos')]"

LOGIN_HEADING = "(//*[self::span or self::h1][normalize-space()='Sign in to X'])[1]"
USERNAME_INPUT = "//input[@autocomplete='username']"
NEXT_BUTTON = "//button[.//span[normalize-space()='Next']]"
FORGOT_PASSWORD_BUTTON = "//button[.//span[normalize-space()='Forgot password?']]"
SIGN_UP_BUTTON = "//button[.//span[normalize-space()='Sign up']]"

RESET_HEADING = "(//*[self::span or self::h1][contains(normalize-space(), 'Find your X account')])[1]"
SIGNUP_HEADING = "(//*[self::span or self::h1][normalize-space()='Create your account'])[1]"
NAME_INPUT = "//input[@name='name']"
PHONE_INPUT = "//input[@name='phone_number']"
EMAIL_INPUT = "//input[@name='email']"
USE_EMAIL_INSTEAD_BUTTON = "//button[.//span[contains(normalize-space(), 'Use email instead')]]"
SIGNUP_NEXT_DISABLED = "//button[@aria-disabled='true' and .//span[normalize-space()='Next']]"


def wait_present(driver: WebDriver, xpath: str):
    return WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def wait_visible(driver: WebDriver, xpath: str):
    return WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def click_xpath(driver: WebDriver, xpath: str) -> None:
    element = wait_present(driver, xpath)
    try:
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: element.is_displayed() and element.is_enabled()
        )
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def element_exists(driver: WebDriver, xpath: str) -> bool:
    return bool(driver.find_elements(By.XPATH, xpath))


def dismiss_cookie_banner(driver: WebDriver) -> None:
    wait_visible(driver, COOKIE_REFUSE_BUTTON)
    click_xpath(driver, COOKIE_REFUSE_BUTTON)
    WebDriverWait(driver, TIMEOUT).until(
        EC.invisibility_of_element_located((By.XPATH, COOKIE_REFUSE_BUTTON))
    )


def test_landing_page_shows_guest_onboarding(driver: WebDriver) -> None:
    driver.get(BASE_URL)

    wait_visible(driver, COOKIE_REFUSE_BUTTON)
    heading = wait_visible(driver, HAPPENING_NOW_HEADING)

    assert heading.text == "Happening now"
    assert element_exists(driver, CREATE_ACCOUNT_LINK)
    assert element_exists(driver, SIGN_IN_LINK)
    assert element_exists(driver, TERMS_OF_SERVICE_LINK)


def test_cookie_banner_can_be_dismissed(driver: WebDriver) -> None:
    driver.get(BASE_URL)

    dismiss_cookie_banner(driver)

    assert not element_exists(driver, COOKIE_REFUSE_BUTTON)
    assert element_exists(driver, HAPPENING_NOW_HEADING)


def test_login_form_is_available(driver: WebDriver) -> None:
    driver.get(LOGIN_URL)

    heading = wait_visible(driver, LOGIN_HEADING)

    assert heading.text == "Sign in to X"
    assert element_exists(driver, USERNAME_INPUT)
    assert element_exists(driver, NEXT_BUTTON)
    assert element_exists(driver, FORGOT_PASSWORD_BUTTON)
    assert element_exists(driver, SIGN_UP_BUTTON)


def test_forgot_password_navigation_opens_reset_flow(driver: WebDriver) -> None:
    driver.get(LOGIN_URL)

    click_xpath(driver, FORGOT_PASSWORD_BUTTON)
    reset_heading = wait_visible(driver, RESET_HEADING)

    assert "Find your X account" in reset_heading.text
    assert element_exists(driver, NEXT_BUTTON)


def test_signup_form_switches_phone_to_email(driver: WebDriver) -> None:
    driver.get(BASE_URL)

    dismiss_cookie_banner(driver)
    click_xpath(driver, CREATE_ACCOUNT_LINK)
    signup_heading = wait_visible(driver, SIGNUP_HEADING)

    assert signup_heading.text == "Create your account"
    assert element_exists(driver, NAME_INPUT)
    assert element_exists(driver, USE_EMAIL_INSTEAD_BUTTON)
    assert element_exists(driver, SIGNUP_NEXT_DISABLED)

    click_xpath(driver, USE_EMAIL_INSTEAD_BUTTON)
    wait_present(driver, EMAIL_INPUT)

    assert element_exists(driver, EMAIL_INPUT)
