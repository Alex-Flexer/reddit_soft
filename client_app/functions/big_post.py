import tkinter as tk
from tkinter import filedialog, messagebox
from time import sleep
from datetime import datetime, timedelta
import os
from shutil import move
import win32clipboard as clip
import win32con
from io import BytesIO
from PIL import Image
from random import randint

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from login import login, slow_typing, rand_sleep, click

from log_windows import LogWindow

from re import findall
from keyring import get_password

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebdriver

from sys import path

path.insert(1, "functions")

from db_funcs import get_reddit_accounts, get_proxy
from proxy import driver_proxy


WebDriver = ChromeWebdriver | FirefoxWebdriver

user_email = None
reddit_account_email = None
reddit_account_password = ""


POST_URL = 'https://www.reddit.com/r/{subreddit}/submit/?type={type}'

PATTERN_ERROR_MESSAGE =\
    "div.items-baseline:nth-child(2) > r-form-validation-message:nth-child(1)"
PATTERN_FLAIR_BUTTON =\
    "#reddit-post-flair-button > span:nth-child(1) > span:nth-child(1)"
PATTERN_SUBMIT_BUTTON = "#submit-post-button"
PATTERN_TITLE_INPUT = "faceplate-textarea-input.rounded-[20px]"
PATTERN_ADD_FLAIR_BUTTON = "#post-flair-modal-apply-button"
PATTERN_FLAIR_SPANS =\
    "div.flex-col > div[name=flairId] > faceplate-radio-input > span"


def copy_image_to_clipboard(image_path: str):
    image = Image.open(image_path)
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_DIB, data)
    clip.CloseClipboard()


def post(
        mouse: ActionChains,
        driver: WebDriver,
        subreddit: str,
        file_path: str,
        title: str,
        flair: str | None = None
) -> tuple[str, bool]:
    copy_image_to_clipboard(file_path)

    post_url = POST_URL.format(subreddit=subreddit, type="IMAGE")
    driver.get(post_url)

    sleep(6)

    current_type = findall(r".*\?type=([A-Z]+)", driver.current_url)

    if "IMAGE" in current_type:
        return "unable to use IMAGE type", False

    title_input_element = driver.find_element(
        By.CSS_SELECTOR, PATTERN_TITLE_INPUT)

    click(mouse, title_input_element)
    rand_sleep()

    slow_typing(title, mouse, 7, 0.9)
    rand_sleep()

    mouse.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    sleep(4)

    flair_button_shadow_root: ShadowRoot = driver.find_element(
        By.CSS_SELECTOR, "#post-flair-modal").shadow_root
    flair_button_span: WebElement = flair_button_shadow_root.find_element(
        By.CSS_SELECTOR, PATTERN_FLAIR_BUTTON)

    flair_button_text: str = flair_button_span.text

    if flair is None and '*' in flair_button_text:
        return "expected flairs", False

    submit_button: WebElement = driver.find_element(
        By.CSS_SELECTOR, PATTERN_SUBMIT_BUTTON)

    if not flair is None:
        original_flair = flair.lower().strip()

        click(mouse, flair_button_span)
        rand_sleep()

        faceplate_dialog_element_root = flair_button_shadow_root.find_element(
            By.CSS_SELECTOR, ".p-0")

        flairs_spans: list[WebElement] = \
            faceplate_dialog_element_root.find_elements(
                By.CSS_SELECTOR, PATTERN_FLAIR_SPANS)

        required_flair_element: WebElement | None = None

        for flair_span in flairs_spans:
            flair_text = flair_span.text.lower().strip()
            if original_flair == flair_text:
                required_flair_element = flair_span
                break

        if required_flair_element is None:
            return f"flair \"{flair}\" was not found", False
        else:
            click(mouse, required_flair_element)
            rand_sleep()

            add_flair_button = faceplate_dialog_element_root.find_element(
                By.CSS_SELECTOR, PATTERN_ADD_FLAIR_BUTTON)
            click(mouse, add_flair_button)
            rand_sleep()

    click(mouse, submit_button)
    rand_sleep()

    start_time = datetime.now()
    while start_time - datetime.now() < timedelta(seconds=20) and "submit" in driver.current_url:
        continue

    if "submit" in driver.current_url:
        error_message = driver.find_element(By.CSS_SELECTOR, PATTERN_ERROR_MESSAGE). \
            shadow_root.find_elements(By.CSS_SELECTOR, "p.m-0")

        if error_message != [] and error_message[0].text != "":
            return error_message.text, False
    else:
        return f"was successfully posted", True


def big_post(subs_path, reddit_email, reddit_password, host, port, user, password):
    driver: WebDriver = driver_proxy(host, port, user, password)
    log_window = LogWindow()

    mouse = ActionChains(driver)
    is_logged_in = login(driver, reddit_email, reddit_password, 0, 0.8, mouse)
    if not is_logged_in:
        log_window.log_message("Unknown login error")
        return

    log_window.log_message("Successfully logged in")

    for subdir in os.listdir(subs_path):
        sub_path = os.path.join(subs_path, subdir)

        subreddit_name = subdir

        good_subdir: bool = True
        if os.path.isdir(sub_path):
            used_path = os.path.join(sub_path, 'used')

            if not os.path.exists(used_path):
                os.makedirs(used_path)

            titles_path: str | None = None
            flairs_path: str | None = None

            titles: list[str] = []
            flairs: list[str] | None = None

            images_paths: list[str] = []

            for file in os.listdir(sub_path):
                file_path = os.path.join(sub_path, file)

                if file.title().lower() == "titles.txt":
                    if len(titles) > 0:
                        log_window.log_message(
                            subreddit_name, "file must contain only one titles file")
                        good_subdir = False
                        break

                    with open(file_path, 'r', encoding='utf-8') as f:
                        titles = f.read().strip().split('\n')
                        titles_path = file_path

                elif file.title().lower() == "flairs.txt":
                    if not flairs is None:
                        log_window.log_message(
                            subreddit_name, "file must contain not more one flairs file")
                        good_subdir = False
                        break

                    with open(file_path, 'r', encoding='utf-8') as f:
                        flairs_not_striped = f.read().strip().split('\n')
                        flairs = list(
                            map(lambda flair: flair.strip(), flairs_not_striped))
                        flairs_path = file_path

                elif file.endswith(".JPG") or file.endswith(".png") or file.endswith(".jpeg"):
                    images_paths.append(file_path)

            if not good_subdir:
                continue

            if len(images_paths) != len(titles):
                log_window.log_message(
                    subreddit_name, "amount of images do not match with amount of titles")
            if not flairs is None and len(images_paths) != len(flairs):
                log_window.log_message(
                    subreddit_name, "amount of images do not match with amount of flairs")
            if not flairs is None and len(titles) != len(flairs):
                log_window.log_message(
                    subreddit_name, "amount of titles do not match with amount of flairs")

            if (not flairs is None and len(titles) != len(flairs)) or len(images_paths) != len(titles):
                continue

            not_posted_titles: list[str] = []
            for ind, image_path in enumerate(images_paths):
                log_window.log_message(
                    f"{subreddit_name}->{titles[ind]}: ", end="")
                try:
                    message, is_successfully_posted = post(mouse, driver, subreddit_name, image_path,
                                                           titles[ind], flairs[ind] if flairs else None)
                    log_window.log_message(titles[ind], message)
                    if is_successfully_posted:
                        image_name = os.path.basename(image_path)
                        move(image_path, os.path.join(
                            sub_path, "used", image_name))
                except Exception as e:
                    log_window.log_message(str(e).lower())
                    not_posted_titles.append(titles[ind])

            with open(titles_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(not_posted_titles))

            if not flairs is None:
                with open(flairs_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(not_posted_titles))

                sleep(randint(8, 20) * 60)

    root.mainloop()


def choose_email_window(update_status_callback):
    """Open a window for choosing an account."""
    global user_email
    accounts, msg = get_reddit_accounts(user_email)

    if accounts is None:
        messagebox.showerror("Error", msg)
        return

    def select_email(email, password):
        global reddit_account_email, reddit_account_password
        reddit_account_email, reddit_account_password = email, password

        messagebox.showinfo("Info", f"Selected Email: {reddit_account_email}")
        update_status_callback()
        email_window.destroy()

    email_window = tk.Tk()
    email_window.title("Choose Email")
    tk.Label(email_window, text="Choose an Email:",
             font=("Arial", 14)).pack(pady=10)

    for account in accounts:
        tk.Button(
            email_window,
            text=account['email'],
            font=("Arial", 12),
            command=lambda e=account["email"], p=account["password"]: select_email(
                e, p)
        ).pack(pady=5)

    email_window.mainloop()


def tkinter_reddit_big_post():
    """GUI for Reddit Big Post."""
    global user_email
    user_email = get_password("user", "email")

    if user_email is None:
        return

    def update_status():
        if reddit_account_email:
            label_selected_account.config(text=f"Selected Account: {
                                          reddit_account_email}", fg="green")
        else:
            label_selected_account.config(text="No account selected", fg="red")

    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    def start_big_post():
        if not reddit_account_email:
            messagebox.showerror("Error", "Please select an account first!")
            return

        subs_path = entry_folder.get()
        if os.path.exists(subs_path):
            proxy, message = get_proxy(reddit_account_email)
            if proxy is None:
                messagebox.showerror("Error", message)
            else:
                big_post(
                    subs_path,
                    reddit_account_email,
                    reddit_account_password,
                    **proxy
                )
            messagebox.showinfo("Success", "Posting started!")
        else:
            messagebox.showerror("Error", "Invalid folder path!")

    root = tk.Tk()
    root.title("Reddit Big Poster")

    tk.Label(root, text="Select Account:").grid(
        row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Choose Account", command=lambda: choose_email_window(
        update_status)).grid(row=0, column=1, padx=10, pady=10)
    label_selected_account = tk.Label(
        root, text="No account selected", fg="red")
    label_selected_account.grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Select subs folder:").grid(
        row=1, column=0, padx=10, pady=10)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_folder).grid(
        row=1, column=2, padx=10, pady=10)

    tk.Button(root, text="Start Posting", command=start_big_post).grid(
        row=2, column=1, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    tkinter_reddit_big_post()
