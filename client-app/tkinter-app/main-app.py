import tkinter as tk
from tkinter import messagebox
import requests
import random
from main_func_app import create_window


confirmation_code = None


def start_registration():
    root = tk.Tk()
    root.title("Регистрация")

    tk.Label(root, text="Логин:").grid(row=0, column=0, padx=10, pady=5)
    entry_login = tk.Entry(root)
    entry_login.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    def submit_login_password():
        login = entry_login.get()
        password = entry_password.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        response = authenticate_user(login, password)

        if response.get("status") == "success":
            root.destroy()
            request_email()
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    tk.Button(root, text="Войти", command=submit_login_password).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()




def request_email():
    root = tk.Tk()
    root.title("Ввод почты")

    tk.Label(root, text="Введите вашу почту:").grid(row=0, column=0, padx=10, pady=5)
    entry_email = tk.Entry(root)
    entry_email.grid(row=0, column=1, padx=10, pady=5)

    def send_code():
        email = entry_email.get()

        if not email:
            messagebox.showerror("Ошибка", "Пожалуйста, введите почту")
            return

        global confirmation_code
        confirmation_code = send_confirmation_code(email)

        root.destroy()
        request_code()

    tk.Button(root, text="Отправить код", command=send_code).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()


def request_code():
    root = tk.Tk()
    root.title("Подтверждение кода")

    tk.Label(root, text="Введите код:").grid(row=0, column=0, padx=10, pady=5)
    entry_code = tk.Entry(root)
    entry_code.grid(row=0, column=1, padx=10, pady=5)

    def verify_code():
        entered_code = entry_code.get()

        if entered_code == str(confirmation_code):
            messagebox.showinfo("Успех", "Подтверждение прошло успешно!")
            root.destroy()
        else:
            messagebox.showerror("Ошибка", "Неправильный код")

    tk.Button(root, text="Подтвердить", command=verify_code).grid(row=1, column=0, columnspan=2, pady=10)

    root.destroy()
    create_window()


# функция отправки кода на почту
def send_confirmation_code():
    print('hello world')


# функция проверки пользователя на наличие
def authenticate_user():
    print('hello world')


# Запуск регистрации
start_registration()
