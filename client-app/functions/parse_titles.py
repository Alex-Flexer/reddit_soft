import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as chrome_webdriver
from selenium.webdriver.firefox.webdriver import WebDriver as firefox_webdriver

from exceptions import AmountTitlesExceptions

import random
import re

WebDriver = chrome_webdriver | firefox_webdriver

MAX_AMOUNT_TITLES = 200

driver = webdriver.Chrome()


def get_random_int(max_value):
    return random.randint(0, max_value - 1)


def modify_titles(filtered_titles):
    modified_titles = []

    for title in filtered_titles:
        new_title = title

        if get_random_int(3) == 0:
            new_title = new_title.replace(" you ", " u ")
        new_title = new_title.replace("you’re", "you are")
        new_title = new_title.replace("You’re ", "You are ")
        new_title = new_title.replace(" can't ", " can not ")
        new_title = new_title.replace("What's ", "What is ")
        new_title = new_title.replace(" you'll ", " you will ")
        new_title = new_title.replace(" i ", " I ")
        new_title = new_title.replace(" hi ", " hey ")
        new_title = new_title.replace(" dick ", " cock ")
        new_title = new_title.replace("I'm ", "I am ")
        new_title = new_title.replace('Say "hi" ', 'Say "yes" ')
        new_title = new_title.replace(" boobs", " tits")
        new_title = new_title.replace(' "hey" ', ' "hi" ')

        modified_titles.append(new_title)

    return modified_titles


def parse_titles(
        subreddit,
        amount_titles: int = 10
) -> list[str]:
    driver = webdriver.Chrome()

    post_url1 = f'http://www.reddit.com/r/{subreddit}/new'

    if amount_titles > MAX_AMOUNT_TITLES:
        raise AmountTitlesExceptions(amount_titles, MAX_AMOUNT_TITLES)

    sleep(3)

    driver.get(post_url1)
    time.sleep(3)

    html = driver.page_source
    titles = re.findall(r'aria-label="([^"]*)"', html)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    to_remove = {
        'Home', 'Notifications', 'Close dialog', 'Shreddit QR', 'Google play', 'App store',
        'Community actions', 'Post distinguished by admin', 'Post distinguished by moderator',
        'Locked post', 'Sticked post', 'Archived post', 'Reddit resources', 'Primary', 'Community information',
        'Edit user flair', "'", '"', 'New rule announcement.',
        f'r/{subreddit} - Join the official amihot Discord server ', 'Join the official amihot Discord server ',
        f'r/{subreddit} - New rule announcement.', '[', ']'
    }
    filtered_titles = [title for title in titles if title not in to_remove]
    filtered_titles = emoji_pattern.sub(r'', str(filtered_titles))
    if not filtered_titles:
        print(f"No titles found on the subreddit '{subreddit}'")
        filtered_titles = 'default title'
    modify_titles(filtered_titles)

    return filtered_titles
