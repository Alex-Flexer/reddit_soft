from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def driver_proxy(host, port, user, password) -> Chrome:
    proxy_options = {
        'proxy': {
            'http': f'http://{user}:{password}@{host}:{port}',
            'https': f'http://{user}:{password}@{host}:{port}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        seleniumwire_options=proxy_options,
        options=options)

    return driver
