from time import sleep

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.webdriver import WebDriver as chrome_webdriver
from selenium.webdriver.firefox.webdriver import WebDriver as firefox_webdriver

from exceptions import AmountTitlesExceptions


WebDriver = chrome_webdriver | firefox_webdriver


MAX_AMOUNT_TITLES = 200


def parse_titles(
        driver: WebDriver,
        subreddit_ind: int = 1,
        amount_titles: int = 10
            ) -> list[str]:

    if amount_titles > MAX_AMOUNT_TITLES:
        raise AmountTitlesExceptions(amount_titles, MAX_AMOUNT_TITLES)

    titles: list[str] = []

    driver.get(f"https://www.reddit.com/?rdt={subreddit_ind}")
    sleep(3)

    title_elements = []

    while len(title_elements) < amount_titles:
        print(len(title_elements))
        title_elements = driver.find_elements(
            by=By.CSS_SELECTOR, value='a[slot="title"]')

        driver.execute_script(
            "arguments[0].scrollIntoView(true);", title_elements[-1])

        sleep(1)

    titles = [title.text for title in title_elements]
    return titles[:amount_titles]
