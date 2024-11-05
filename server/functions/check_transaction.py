from time import sleep

from keyring import get_password as get_secret_value

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


RECIPIENT_TOKEN = get_secret_value("common", "CRYPTO_TOKEN")


def check_transaction(amount: float, currency: str = "TRX") -> bool:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(f"https://tronscan.org/#/address/{RECIPIENT_TOKEN}")

    sleep(6)

    try:
        table_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tab_data_list"))
        )
    except TimeoutException:
        print("Element was not found")
        driver.quit()
        return False

    table = table_frame.find_element(By.TAG_NAME, "tbody")
    driver.execute_script("arguments[0].scrollIntoView(true);", table)
    sleep(0.3)

    lines = table.find_elements(By.TAG_NAME, "tr")
    for line in lines:
        cells = line.find_elements(By.TAG_NAME, "td")
        transaction_age_str, value_str = cells[3].text, cells[8].text

        if "day" in transaction_age_str:
            break

        value = float(value_str.replace(currency, ''))

        if currency in value_str and value == amount:
            return True

    driver.delete_all_cookies()
    driver.quit()
    return False
