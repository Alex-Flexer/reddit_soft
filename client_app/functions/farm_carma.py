import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from random import randint, uniform, random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from login import login, click
from log_windows import LogWindow
from bisect import bisect_left
from keyring import get_password
from db_funcs import get_reddit_accounts
from proxy import driver_proxy
from selenium.webdriver.common.action_chains import ActionChains

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
            ReactionSection(upvote_button, downvote_button,
                            upvote_button.location['y'])
        )


def mark_reaction(logger: LogWindow, mouse: ActionChains, driver: WebDriver, upvote_chance: float, y_position: int):
    section_ind = bisect_left(reaction_section_list,
                              y_position, key=lambda section: section.y)
    if section_ind >= len(reaction_section_list):
        reload_reaction_sections(driver)

    section_ind = bisect_left(reaction_section_list,
                              y_position, key=lambda section: section.y)
    if random() <= upvote_chance:
        try:
            click(mouse, reaction_section_list[section_ind].upvote_button)
        except ElementClickInterceptedException:
            try:
                click(
                    mouse, reaction_section_list[section_ind - 1].upvote_button)
            except ElementClickInterceptedException:
                logger.log_message("Failed attempt to upvote")
        else:
            logger.log_message("Successful upvote")
    else:
        try:
            click(mouse, reaction_section_list[section_ind].downvote_button)
        except ElementClickInterceptedException:
            try:
                click(
                    mouse, reaction_section_list[section_ind - 1].downvote_button)
            except ElementClickInterceptedException:
                logger.log_message("Failed attempt to downvote")
        else:
            logger.log_message("Successful downvote")


def smooth_scroll_reddit_posts(driver: WebDriver, max_scroll_height: int) -> int:
    max_step = 150
    min_step = 10
    pause_chance = 0.1
    max_pause = 1.5

    current_scroll_delta = 0

    while current_scroll_delta < max_scroll_height:
        step = randint(min_step, max_step)
        driver.execute_script(f"window.scrollBy(0, {step});")
        current_scroll_delta += step

        if random() < pause_chance:
            pause_duration = uniform(0.3, max_pause)
            sleep(pause_duration)

        scroll_speed = uniform(0.02, 0.10) \
            if current_scroll_delta < max_scroll_height * 0.8 else uniform(0.08, 0.15)

        sleep(scroll_speed)

    return current_scroll_delta


def farm_carma(logger: LogWindow, mouse: ActionChains, driver: WebDriver, end_time: datetime):
    try:
        logger.log_message("Logging in...")
        login_res = login(mouse, driver, reddit_account_email,
                          reddit_account_password, 0, 0.8)
    except Exception as e:
        logger.log_message(e)
        return

    if not login_res:
        logger.log_message("Unknown login error")
        return

    current_scroll_position = 0

    driver.get("https://reddit.com/")
    sleep(8)

    while datetime.now() < end_time:
        try:
            current_scroll_position += smooth_scroll_reddit_posts(
                driver, randint(800, 1000))
            sleep(uniform(0.3, 1.2))
            try:
                mark_reaction(logger, mouse, driver, 0.7,
                              current_scroll_position)
            except Exception:
                logger.log_message("Failed attempt to vote")

            sleep(uniform(1, 2))
        except Exception as e:
            logger.log_message(e)
            return


def choose_email_window(update_status_callback):
    """Open a window for choosing an account."""
    global user_email
    user_email = get_password("user", "email")

    if user_email is None:
        return
    accounts, msg = get_reddit_accounts(user_email)

    if accounts is None:
        messagebox.showerror("Error", msg)
        return

    def select_email(email, password):
        global reddit_account_email, reddit_account_password
        reddit_account_email = email
        reddit_account_password = password
        messagebox.showinfo("Info", f"Selected Email: {reddit_account_email}")
        update_status_callback()
        email_window.destroy()

    email_window = tk.Tk()
    email_window.title("Choose Email")
    tk.Label(email_window, text="Choose an Email:",
             font=("Modern No. 20", 14)).pack(pady=10)

    for account in accounts:
        tk.Button(
            email_window,
            text=account['email'],
            font=("Modern No. 20", 12),
            command=lambda e=account["email"], p=account["password"]: select_email(
                e, p)
        ).pack(pady=5)

    email_window.mainloop()


def tkinter_reddit_farm():
    global reddit_account_email, reddit_account_password

    def update_status():
        if reddit_account_email:
            label_selected_account.config(text=f"Selected Account: {
                                          reddit_account_email}", fg="green")
        else:
            label_selected_account.config(text="No account selected", fg="red")

    def start_farming():
        if not reddit_account_email:
            messagebox.showerror("Error", "Please select an account first!")
            return

        root.destroy()

        driver = webdriver.Chrome()
        mouse = ActionChains(driver)
        logger = LogWindow()
        farming_thread =\
            Thread(
                target=farm_carma,
                args=(
                    logger,
                    mouse,
                    driver,
                    datetime.now() + timedelta(hours=1),
                ),
                daemon=True
            )
        farming_thread.start()
        logger.run()

    root = tk.Tk()
    root.title("Reddit Karma Farmer")

    tk.Label(
        root,
        text="Select Account:",
        font=("Modern No. 20", 18)
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        root,
        text="Choose Account",
        font=("Modern No. 20", 18),
        command=lambda: choose_email_window(update_status)
    ).grid(row=0, column=1, padx=10, pady=10)

    label_selected_account =\
        tk.Label(
            root,
            text="No account selected",
            font=("Modern No. 20", 18),
            fg="red"
        )

    label_selected_account.grid(row=0, column=2, padx=10, pady=10)

    tk.Button(
        root,
        text="Start Farming",
        font=("Modern No. 20", 18),
        command=start_farming
    ).grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()
