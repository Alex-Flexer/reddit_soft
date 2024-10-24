from time import sleep
from datetime import datetime, timedelta
from random import randint, uniform, random
from bisect import bisect_left

from login import login

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

# from exceptions import LoginError

WebDriver = ChromeWebdriver | FirefoxWebdriver


class ReactionSection:
    upvote_button: WebElement | None
    downvote_button: WebElement | None
    y: int

    def __init__(self, upvote_button: WebElement, downvote_button: WebElement, y: int):
        self.upvote_button = upvote_button
        self.downvote_button = downvote_button
        self.y = y


reaction_section_list: list[ReactionSection] = []


def reload_reaction_sections(driver: WebDriver) -> None:
    driver.get("https://reddit.com/")
    reaction_section_list.clear()

    sleep(4)

    shadow_hosts = driver.find_elements(By.CSS_SELECTOR, 'shreddit-post')

    for shadow_host in shadow_hosts:
        shadow_root = shadow_host.shadow_root
        buttons = shadow_root.find_elements(By.CSS_SELECTOR, 'span > button')

        upvote_button: WebElement | None = None
        downvote_button: WebElement | None = None

        for but in buttons:
            if "upvote" in but.get_attribute("class"):
                upvote_button = but
            elif "downvote" in but.get_attribute("class"):
                downvote_button = but

        reaction_section_list.append(
            ReactionSection(upvote_button, downvote_button, upvote_button.location['y'])
        )



def mark_reaction(driver: WebDriver, upvote_chance: float, y_position: int):
    section_ind = bisect_left(reaction_section_list, y_position, key=lambda section: section.y)
    if section_ind >= len(reaction_section_list):
        reload_reaction_sections(driver)

    section_ind = bisect_left(reaction_section_list, y_position, key=lambda section: section.y)
    if random() <= upvote_chance:
        reaction_section_list[section_ind].upvote_button.click()
    else:
        reaction_section_list[section_ind].downvote_button.click()


def smooth_scroll_reddit_posts(driver: WebDriver, max_scroll_height: int) -> int:
    max_step = 150
    min_step = 10
    pause_chance = 0.1
    max_pause = 1.5

    current_scroll_position = 0

    while current_scroll_position < max_scroll_height:
        step = randint(min_step, max_step)
        step = step

        driver.execute_script(f"window.scrollBy(0, {step});")
        current_scroll_position += step

        if random() < pause_chance:
            pause_duration = uniform(0.3, max_pause)
            sleep(pause_duration)

        scroll_speed = uniform(0.02, 0.10) \
            if current_scroll_position < max_scroll_height * 0.8 else uniform(0.08, 0.15)

        sleep(scroll_speed)

    return current_scroll_position


def farm_carma(driver: WebDriver, end_time: datetime):
    while datetime.now() < end_time:
        current_scroll_position = smooth_scroll_reddit_posts(driver, randint(1, 500))

        sleep(uniform(0.1, 1))
        mark_reaction(driver, uniform(0.4, 0.7), current_scroll_position)
        sleep(uniform(0.4, 0.6))

    driver.quit()

if __name__ == '__main__':
    driver = webdriver.Firefox()
    login(driver, "email", "password")
    farm_carma(driver, datetime.now() + timedelta(seconds=20))
