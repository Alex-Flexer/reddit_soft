from time import sleep
from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver

from exceptions import LoginError


WebDriver = ChromeWebdriver | FirefoxWebdriver


def slow_typing(text: str, mouse: ActionChains) -> None:
    for letter in text:
        mouse.send_keys(letter).perform()
        sleep(randint(10, 200) / 200)


def rand_sleep() -> None:
    sleep(randint(10, 100) / 100)


def login(driver: WebDriver, username: str, password: str) -> None:
    mouse = ActionChains(driver)

    driver.get("https://www.reddit.com/login/")

    sleep(3)

    login_input = driver.find_element(By.ID, "login-username")
    password_input = driver.find_element(By.ID, "login-password")

    mouse.move_to_element(login_input).perform()
    rand_sleep()

    mouse.click().perform()
    rand_sleep()

    slow_typing(username, mouse)
    rand_sleep()

    mouse.move_to_element(password_input).perform()
    rand_sleep()

    mouse.click().perform()
    rand_sleep()

    slow_typing(password, mouse)
    rand_sleep()

    mouse.send_keys(Keys.ENTER).perform()

    sleep(10)

    if "login" in driver.current_url:
        raise LoginError
