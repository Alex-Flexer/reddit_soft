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

driver = webdriver.Edge()


def big_post(subs_path):
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
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')
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
                elem = driver.find_element(By.CSS_SELECTOR,
                                           '#innerTextArea')
                # add title

                elem.send_keys(title + Keys.RETURN)

                pyperclip.copy(photo_path)

                driver.find_element(By.CSS_SELECTOR,
                                    '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > '
                                    'div._31N0dvxfpsO6Ur5AKx4O5d > '
                                    'div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1'
                                    '.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA > div.HOFZo2X7Fr6JVBztpsByj > '
                                    'div._3w_665DK_NH7yIsRMuZkqB > div._1zq6UabIEJJ-z9grsiCJY7 > '
                                    'div._1UbcPNs4A8n5PIWX0H5sGt > div > div > div > p > button').click()
                # click upload button

                time.sleep(1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR,
                                    '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > '
                                    'div._31N0dvxfpsO6Ur5AKx4O5d > '
                                    'div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1'
                                    '.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA > div.HOFZo2X7Fr6JVBztpsByj > '
                                    'div._3w_665DK_NH7yIsRMuZkqB > div._1d1--0DMy_jAIxCCoYMo1k > '
                                    'div._2pAQpGYEPAVsPmV5uVmGGU >'
                                    'div > button:nth-child(3)').click()  # add photo path

                shutil.move(photo_path, os.path.join(used_path, file))  # move to used

            except NoSuchElementException as e:
                print(f"Element not found while processing subreddit '{subreddit}': {e}")

            except Exception as e:
                print(f"An error occurred while processing subreddit '{subreddit}': {e}")


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
