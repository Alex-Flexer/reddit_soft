import tkinter as tk
from tkinter import messagebox
from requests import ConnectionError, post as post_request
from json import dumps

from main_func_app import create_window

user_email: str | None = None

root = None

def start_registration():
    root = tk.Tk()
    root.title("Registration")

    tk.Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=5)
    entry_email = tk.Entry(root)
    entry_email.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    def submit_login_password():
        global user_email

        email = entry_email.get()
        password = entry_password.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill the required fields")
            return

        response_json = authenticate_user(email, password)

        if response_json is None:
            messagebox.showerror("Error", "Network error")
        elif response_json["result"]:
            user_email = email
            root.destroy()
            request_code()
        else:
            messagebox.showerror("Error", response_json["message"])

    tk.Button(root, text="Войти", command=submit_login_password).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()


def request_code():
    print("start request code")
    response_json = send_confirmation_code(user_email)

    if response_json is None or not response_json["result"]:
        if response_json is None:
            messagebox.showerror("Error", "Network error")
        else:
            messagebox.showerror("Error", response_json["message"])

        root.destroy()
        return

    root = tk.Tk()
    root.title("Confirm Email Code")

    tk.Label(root, text="Enter your email code:").grid(row=0, column=0, padx=10, pady=5)
    entry_code = tk.Entry(root)
    entry_code.grid(row=0, column=1, padx=10, pady=5)

    def verify_code():
        entered_code = entry_code.get()

        data = dumps({"email": user_email, "code": entered_code})
        try:
            response = post_request("http://127.0.0.1:8000/confirm/email-code", data=data)
            response_json = response.json()
        except ConnectionError:
            messagebox.showerror("Error", "Nerwork error")
        else:
            if response_json["result"]:
                messagebox.showinfo("Success", "Your email code is successfully confirmed!")
                root.destroy()
            else:
                messagebox.showerror("Error", response_json["message"])

    tk.Button(root, text="Confirm", command=verify_code).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()
    root.destroy()

    create_window()


# функция отправки кода на почту
def send_confirmation_code(email: str):
    data = dumps({"email": email})
    try:
        response = post_request("http://127.0.0.1:8000/send/email-code/", data=data)
        json = response.json()
    except ConnectionError:
        json = None
    finally:
        return json


def authenticate_user(email: str, password: str) -> dict | None:
    data = dumps({"email": email, "password": password})

    try:
        response = post_request("http://127.0.0.1:8000/login/user", data=data)
        json = response.json()
    except ConnectionError:
        json = None
    finally:
        return json


if __name__ == "__main__":
    start_registration()
