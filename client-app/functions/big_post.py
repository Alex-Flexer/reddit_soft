import os
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from login import login
import pyperclip
import pyautogui
import shutil
import time


def big_post(subs_path):
    driver = webdriver.Edge()
    login(driver, 'example', 'example')

    for subdir in os.listdir(subs_path):
        sub_path = os.path.join(subs_path, subdir)

        if os.path.isdir(sub_path):
            title = ""
            photo_path = ""
            subreddit = subdir
            used_path = os.path.join(sub_path, 'used')

            if not os.path.exists(used_path):
                os.makedirs(used_path)

            for file in os.listdir(sub_path):
                file_path = os.path.join(sub_path, file)

                if file.endswith(".txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        title = f.read().strip()

                if file.endswith(".JPG") or file.endswith(".png") or file.endswith(".jpeg"):
                    photo_path = file_path

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation confirmation popup to appear.')
                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
            except TimeoutException:
                print("no alert")

            try:
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])

                post_url = f'https://www.reddit.com/r/{subreddit}/submit/?type=IMAGE'
                driver.get(post_url)
                time.sleep(1)

                elem = driver.find_element(By.CSS_SELECTOR, '#innerTextArea')
                # Add title
                elem.send_keys(title + Keys.RETURN)

                pyperclip.copy(photo_path)

                driver.find_element(By.CSS_SELECTOR, 'YOUR_UPLOAD_BUTTON_SELECTOR').click()  # Update selector
                time.sleep(1)

                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, 'YOUR_SUBMIT_BUTTON_SELECTOR').click()  # Update selector
                shutil.move(photo_path, os.path.join(used_path, file))  # Move to used

            except NoSuchElementException as e:
                print(f"Element not found while processing subreddit '{subreddit}': {e}")
            except Exception as e:
                print(f"An error occurred while processing subreddit '{subreddit}': {e}")

    driver.quit()


def tkinter_reddit_big_post():
    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    def start_big_post():
        subs_path = entry_folder.get()
        if os.path.exists(subs_path):
            big_post(subs_path)
            messagebox.showinfo("Success", "Posting completed!")
        else:
            messagebox.showerror("Error", "Invalid folder path!")

    root = tk.Tk()
    root.title("Reddit Big Poster")

    tk.Label(root, text="Select subs folder:").grid(row=0, column=0, padx=10, pady=10)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_folder).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(root, text="Start Posting", command=start_big_post).grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()
