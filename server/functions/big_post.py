import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pyperclip

driver = webdriver.Chrome()


def big_post(title, photo_path, subreddit):
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

        post_url = f'https://new.reddit.com/r/{subreddit}/submit/?type=IMAGE'

        driver.get(post_url)
        time.sleep(1)

        elem = driver.find_element(By.CSS_SELECTOR,
                                   '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > '
                                   'div._31N0dvxfpsO6Ur5AKx4O5d > '
                                   'div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1'
                                   '.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA > div.HOFZo2X7Fr6JVBztpsByj > '
                                   'div._3w_665DK_NH7yIsRMuZkqB > div._1zq6UabIEJJ-z9grsiCJY7 > '
                                   'div._3zkbHfhLbXp21FwGj_kNZV > div > textarea')
        elem.send_keys(title + Keys.RETURN)
        print('Title inserted')

        pyperclip.copy(photo_path)

        driver.find_element(By.CSS_SELECTOR,
                            '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > '
                            'div._31N0dvxfpsO6Ur5AKx4O5d > '
                            'div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1'
                            '.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA > div.HOFZo2X7Fr6JVBztpsByj > '
                            'div._3w_665DK_NH7yIsRMuZkqB > div._1zq6UabIEJJ-z9grsiCJY7 > '
                            'div._1UbcPNs4A8n5PIWX0H5sGt > div > div > div > p > button').click()  # upload button
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        print('photo inserted')
        driver.find_element(By.CSS_SELECTOR,
                            '#AppRouter-main-content > div > div > div._3ozFtOe6WpJEMUtxDOIvtU > '
                            'div._31N0dvxfpsO6Ur5AKx4O5d > '
                            'div._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1'
                            '.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA > div.HOFZo2X7Fr6JVBztpsByj > '
                            'div._3w_665DK_NH7yIsRMuZkqB > div._1d1--0DMy_jAIxCCoYMo1k > div._2pAQpGYEPAVsPmV5uVmGGU > '
                            'div > button:nth-child(3)').click()

    except NoSuchElementException as e:
        print(f"Element not found while processing subreddit '{subreddit}': {e}")

    except Exception as e:
        print(f"An error occurred while processing subreddit '{subreddit}': {e}")
