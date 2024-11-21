from seleniumwire import webdriver


def driver_proxy(proxy_host, proxy_port, proxy_user, proxy_password):
    proxy_options = {
        'proxy': {
            'http': f'http://{proxy_user}:{proxy_password}@{proxy_host}:{proxy_port}',
            'https': f'http://{proxy_user}:{proxy_password}@{proxy_host}:{proxy_port}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    driver = webdriver.Chrome(seleniumwire_options=proxy_options)

    return driver
