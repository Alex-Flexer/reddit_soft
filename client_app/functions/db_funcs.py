from json import dumps
from requests import post


def send_credentials(email: str, password: str) -> dict[str, str] | None:
    json_response = None
    json = dumps({"email": email, "password": password})
    try:
        response = post(
            "http://reddsyndicate.com/add/reddit-account/", data=json)
        json_response = response.json()
    finally:
        return json_response


def send_proxy(host: str, port: str, password: str, user: str) -> dict[str, str] | None:
    json_response = None
    json = dumps({"host": host, "port": port,
                 "password": password, "user": user})
    try:
        response = post("http://reddsyndicate.com/set/proxy", data=json)
        json_response = response.json()
    finally:
        return json_response


def get_proxy(email: str) -> dict[str, str]:
    json_response = None
    json = dumps({"email": email})
    try:
        response = post("http://reddsyndicate.com/get/proxy", data=json)
        json_response = response.json()
    finally:
        return json_response


def get_reddit_accounts(user_email: str) -> list[dict[str, str]]:
    json_response = None
    json = dumps({"email": user_email})
    try:
        response = post(
            "http://reddsyndicate.com/get/reddit-accounts", data=json)
        json_response = response.json()
    finally:
        return json_response
