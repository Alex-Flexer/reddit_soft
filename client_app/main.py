from tkinter import messagebox

from keyring import get_password as get_secret_value
from requests import post
from json import dumps

from main_app import start_registration
from main_func_app import create_window


def check_user(email, password, token):
    data = dumps({"email": email, "password": password, "token": token})
    try:
        response = post("http://127.0.0.1:8000/check/user-credentials/", data=data)
        json = response.json()
    except ConnectionError:
        json = None
    finally:
        return json

def main():
    email = get_secret_value("user", "email")
    password = get_secret_value("user", "password")
    token = get_secret_value("user", "token")

    if not email or not password or not token:
        start_registration()
        return
    else:
        response_json = check_user(email, password, token)
        if response_json is None:
            messagebox.showerror("Error", "Network error")
        elif not response_json["result"]:
            messagebox.showerror("Error", response_json["message"])
        else:
            create_window()

if __name__ == "__main__":
    main()