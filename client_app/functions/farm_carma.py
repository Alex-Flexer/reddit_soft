from time import sleep
from datetime import datetime, timedelta
from random import randint, uniform, random
from bisect import bisect_left

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

import tkinter as tk
from tkinter import messagebox

from login import login


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


def tkinter_karma_farm():
    def start_farming():
        email = entry_email.get()
        password = entry_password.get()
        duration = int(entry_duration.get())

        if not email or not password or not duration:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            driver = webdriver.Chrome()  # или webdriver.Firefox()
            login(driver, email, password)

            end_time = datetime.now() + timedelta(seconds=duration)
            farm_carma(driver, end_time)

            messagebox.showinfo("Success", "Farming completed!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Karma Farmer")

    tk.Label(root, text="Email:", font=("Modern No. 20", 18)).grid(row=0, column=0, padx=10, pady=5)
    entry_email = tk.Entry(root)
    entry_email.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Password:", font=("Modern No. 20", 18)).grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Duration (seconds):", font=("Modern No. 20", 18)).grid(row=2, column=0, padx=10, pady=5)
    entry_duration = tk.Entry(root)
    entry_duration.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(root, text="Start Farming", font=("Modern No. 20", 18), command=start_farming).grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()