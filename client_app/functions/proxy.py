from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome


def driver_proxy(host, port, user, password) -> Chrome:
    proxy_options = {
        'proxy': {
            'http': f'http://{user}:{password}@{host}:{port}',
            'https': f'http://{user}:{password}@{host}:{port}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    driver = webdriver.Chrome(seleniumwire_options=proxy_options)

    return driver
