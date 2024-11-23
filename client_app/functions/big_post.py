import tkinter as tk
from tkinter import filedialog, messagebox
from time import sleep
from datetime import datetime, timedelta
import os
from re import findall
from shutil import move
import win32clipboard as clip
import win32con
from io import BytesIO
from PIL import Image
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.shadowroot import ShadowRoot
from login import login, slow_typing, rand_sleep, click
from log_windows import LogWindow

# Global Variables
user_email = None
user_password = None

POST_URL = 'https://www.reddit.com/r/{subreddit}/submit/?type={type}'
PATTERN_ERROR_MESSAGE = "div.items-baseline:nth-child(2) > r-form-validation-message:nth-child(1)"
PATTERN_TITLE_INPUT = "faceplate-textarea-input.rounded-[20px]"
PATTERN_SUBMIT_BUTTON = "#submit-post-button"


def copy_image_to_clipboard(image_path: str):
    """Copy an image to clipboard."""
    image = Image.open(image_path)
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_DIB, data)
    clip.CloseClipboard()


def choose_email_window(update_status_callback):
    """Open a window for choosing an account."""
    accounts = [
        {"email": "asdf1@example.com", "password": "password1"},
        {"email": "asdf2@example.com", "password": "password2"},
        {"email": "asdf3@example.com", "password": "password3"},
    ]

    def select_email(email, password):
        global user_email, user_password
        user_email, user_password = email, password
        messagebox.showinfo("Info", f"Selected Email: {user_email}")
        update_status_callback()
        email_window.destroy()

    email_window = tk.Tk()
    email_window.title("Choose Email")
    tk.Label(email_window, text="Choose an Email:", font=("Arial", 14)).pack(pady=10)

    for account in accounts:
        tk.Button(
            email_window,
            text=account['email'],
            font=("Arial", 12),
            command=lambda e=account['email'], p=account['password']: select_email(e, p)
        ).pack(pady=5)

    email_window.mainloop()


def post(mouse, driver, subreddit, file_path, title):
    """Post an image on Reddit."""
    copy_image_to_clipboard(file_path)
    post_url = POST_URL.format(subreddit=subreddit, type="IMAGE")
    driver.get(post_url)

    sleep(6)
    title_input_element = driver.find_element(By.CSS_SELECTOR, PATTERN_TITLE_INPUT)
    click(mouse, title_input_element)
    rand_sleep()
    slow_typing(title, mouse, 7, 0.9)
    rand_sleep()
    mouse.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    sleep(4)

    submit_button = driver.find_element(By.CSS_SELECTOR, PATTERN_SUBMIT_BUTTON)
    click(mouse, submit_button)
    rand_sleep()

    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < 20 and "submit" in driver.current_url:
        continue

    if "submit" in driver.current_url:
        return "Error occurred while posting", False
    return "Post successful", True


def big_post(subs_path):
    """Main posting logic."""
    driver = webdriver.Chrome()
    log_window = LogWindow()

    if not login(driver, user_email, user_password, 0, 0.8):
        log_window.log_message("Login failed")
        return

    log_window.log_message("Logged in successfully")
    mouse = ActionChains(driver)

    for subdir in os.listdir(subs_path):
        sub_path = os.path.join(subs_path, subdir)
        if not os.path.isdir(sub_path):
            continue

        images_paths = [os.path.join(sub_path, f) for f in os.listdir(sub_path) if f.lower().endswith((".jpg", ".png"))]
        titles = [f"Title {i + 1}" for i in range(len(images_paths))]

        for img, title in zip(images_paths, titles):
            log_window.log_message(f"Posting to {subdir}: {title}")
            try:
                message, success = post(mouse, driver, subdir, img, title)
                log_window.log_message(message)
                if success:
                    move(img, os.path.join(sub_path, "used", os.path.basename(img)))
            except Exception as e:
                log_window.log_message(f"Error: {str(e)}")


def tkinter_reddit_big_post():
    """GUI for Reddit Big Post."""
    global user_email

    def update_status():
        if user_email:
            label_selected_account.config(text=f"Selected Account: {user_email}", fg="green")
        else:
            label_selected_account.config(text="No account selected", fg="red")

    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    def start_big_post():
        if not user_email:
            messagebox.showerror("Error", "Please select an account first!")
            return

        subs_path = entry_folder.get()
        if os.path.exists(subs_path):
            big_post(subs_path)
            messagebox.showinfo("Success", "Posting completed!")
        else:
            messagebox.showerror("Error", "Invalid folder path!")

    root = tk.Tk()
    root.title("Reddit Big Poster")

    tk.Label(root, text="Select Account:").grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Choose Account", command=lambda: choose_email_window(update_status)).grid(row=0, column=1, padx=10, pady=10)
    label_selected_account = tk.Label(root, text="No account selected", fg="red")
    label_selected_account.grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Select subs folder:").grid(row=1, column=0, padx=10, pady=10)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_folder).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(root, text="Start Posting", command=start_big_post).grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()


tkinter_reddit_big_post()
