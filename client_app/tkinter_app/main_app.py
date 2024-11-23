import tkinter as tk
from tkinter import messagebox
from requests import ConnectionError, post
from json import dumps
from keyring import set_password as set_secret_value, get_password
from db_funcs import send_proxy, send_credentials
user_email: str | None = None
user_password: str | None = None

root: None | tk.Tk = None


def save_credentials() -> None:
    token = update_token(user_email)
    if token is None:
        return
    set_secret_value("user", "email", user_email)
    set_secret_value("user", "password", user_password)
    set_secret_value("user", "token", token)


def get_user_email():
    return get_password("user", "email")


def update_token(email: str) -> None | str:
    data = dumps({"email": email})
    try:
        response = post("http://reddsyndicate.com/update/user-token/", data=data)
        json = response.json()
    except ConnectionError:
        messagebox.showerror("Error", "Network error")
    else:
        if not json["result"]:
            messagebox.showerror("Error", json["message"])
        else:
            return json["token"]


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
        global user_email, user_password
        nonlocal entry_password, entry_email

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
            user_password = password

            root.destroy()
            request_code()

        else:
            messagebox.showerror("Error", response_json["message"])

    tk.Button(root, text="Войти", command=submit_login_password).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()


def request_code():
    global root

    root = tk.Tk()
    root.title("Confirm Email Code")

    tk.Label(root, text="Enter your email code:").grid(row=0, column=0, padx=10, pady=5)
    entry_code = tk.Entry(root)
    entry_code.grid(row=0, column=1, padx=10, pady=5)

    def verify_code():
        entered_code = entry_code.get()

        data = dumps({"email": user_email, "code": entered_code})
        try:
            response = post("http://reddsyndicate.com/confirm/email-code", data=data)
            response_json = response.json()
        except ConnectionError:
            messagebox.showerror("Error", "Network error")
        else:
            if response_json["result"]:
                messagebox.showinfo("Success", "Your email code is successfully confirmed!")
                save_credentials()
                root.destroy()
                login_credentials_window()
            else:
                messagebox.showerror("Error", response_json["message"])

    tk.Button(root, text="Confirm", command=verify_code).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()


def login_credentials_window():
    login_window = tk.Tk()
    login_window.title("User Credentials")

    tk.Label(login_window, text="Login:").grid(row=0, column=0, padx=10, pady=5)
    entry_login = tk.Entry(login_window)
    entry_login.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    def submit_user_credentials():
        user_login = entry_login.get()
        user_pass = entry_password.get()

        if not user_login or not user_pass:
            messagebox.showerror("Error", "Please fill all fields")
            return

        send_credentials(user_login, user_pass)
        login_window.destroy()
        proxy_credentials_window()

    tk.Button(login_window, text="Submit", command=submit_user_credentials).grid(row=2, column=0, columnspan=2, pady=10)
    login_window.mainloop()


def proxy_credentials_window():
    proxy_window = tk.Tk()
    proxy_window.title("Proxy Configuration")

    tk.Label(proxy_window, text="Proxy Host:").grid(row=0, column=0, padx=10, pady=5)
    entry_host = tk.Entry(proxy_window)
    entry_host.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(proxy_window, text="Proxy Port:").grid(row=1, column=0, padx=10, pady=5)
    entry_port = tk.Entry(proxy_window)
    entry_port.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(proxy_window, text="Proxy User:").grid(row=2, column=0, padx=10, pady=5)
    entry_user = tk.Entry(proxy_window)
    entry_user.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(proxy_window, text="Proxy Password:").grid(row=3, column=0, padx=10, pady=5)
    entry_password = tk.Entry(proxy_window, show="*")
    entry_password.grid(row=3, column=1, padx=10, pady=5)

    def submit_proxy_credentials():
        proxy_host = entry_host.get()
        proxy_port = entry_port.get()
        proxy_user = entry_user.get()
        proxy_password = entry_password.get()

        if not all([proxy_host, proxy_port, proxy_user, proxy_password]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        send_proxy(proxy_host, proxy_port, proxy_user, proxy_password)

        proxy_window.destroy()

    tk.Button(proxy_window, text="Submit", command=submit_proxy_credentials).grid(row=4, column=0, columnspan=2, pady=10)
    proxy_window.mainloop()



def authenticate_user(email: str, password: str) -> dict | None:
    data = dumps({"email": email, "password": password})
    json = None

    try:
        response = post("http://reddsyndicate.com/login/user", data=data)
        json = response.json()
    finally:
        return json

if __name__ == '__main__':
    start_registration()
