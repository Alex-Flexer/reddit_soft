from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def check_transaction(from_addreass: str, to_address: str, amount: int, currecy: str = "TRX") -> bool:
    driver = webdriver.Firefox()
    driver.get(f"https://tronscan.org/#/address/{to_address}")

    sleep(6)

    try:
        table_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tab_data_list"))
        )
    except TimeoutException as e:
        print("Element was not found")
        driver.quit()
        return False

    table = table_frame.find_element(By.TAG_NAME, "tbody")
    driver.execute_script("arguments[0].scrollIntoView(true);", table)
    sleep(0.3)

    lines = table.find_elements(By.TAG_NAME, "tr")
    for line in lines:
        cells = line.find_elements(By.TAG_NAME, "td")
        transaction_age_str, address_from_str, value = cells[3].text, cells[5].text, cells[8].text

        if "day" in transaction_age_str:
            break

        if address_from_str.replace('\n', '') == from_addreass:
            if currecy in value and int(value.replace(currecy, '')) == amount:
                return True

    sleep(2)
    driver.quit()
    return False
