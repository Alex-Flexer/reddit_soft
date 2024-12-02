from big_post import big_post
from db_funcs import get_reddit_accounts, get_proxy
import tkinter as tk
from tkinter import filedialog, messagebox
from time import sleep
from datetime import datetime, timedelta
import os
from sys import path
import threading
from keyring import get_password


path.insert(1, "functions")
# from proxy import driver_proxy


user_email = None
reddit_account_email = None
reddit_account_password = ""


def choose_email_window(update_status_callback):
    """Open a window for choosing an account."""
    global user_email
    user_email = get_password("user", "email")

    if user_email is None:
        return
    accounts, msg = get_reddit_accounts(user_email)

    if accounts is None:
        messagebox.showerror("Error", msg)
        return

    def select_email(email, password):
        global reddit_account_email, reddit_account_password
        reddit_account_email = email,
        reddit_account_password = password

        messagebox.showinfo("Info", f"Selected Email: {reddit_account_email}")
        update_status_callback()
        email_window.destroy()

    email_window = tk.Tk()
    email_window.title("Choose Email")
    tk.Label(email_window, text="Choose an Email:",
             font=("Modern No. 20", 14)).pack(pady=10)

    for account in accounts:
        tk.Button(
            email_window,
            text=account['email'],
            font=("Modern No. 20", 12),
            command=lambda e=account["email"], p=account["password"]: select_email(
                e, p)
        ).pack(pady=5)

    email_window.mainloop()


def tkinter_reddit_big_post_with_delay():
    global user_email

    def update_status():
        if reddit_account_email:
            label_selected_account.config(text=f"Selected Account: {
                                          reddit_account_email}", fg="green")
        else:
            label_selected_account.config(text="No account selected", fg="red")

    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    def wait_until(start_time):
        now = datetime.now()
        start_datetime =\
            datetime.combine(now.date(), datetime.strptime(
                start_time, "%H:%M").time())

        if start_datetime < now:
            start_datetime += timedelta(days=1)

        wait_seconds = (start_datetime - now).total_seconds()
        log_window.log_message(f"Waiting until {start_time} to start...")
        sleep(wait_seconds)

    def start_big_post():
        if not reddit_account_email:
            messagebox.showerror("Error", "Please select an account first!")
            return

        subs_path = entry_folder.get()
        if os.path.exists(subs_path):
            start_time = entry_time.get()
            try:
                # Run the waiting in a separate thread to keep the UI responsive
                threading.Thread(
                    target=lambda: (
                        wait_until(start_time),
                        run_big_post(subs_path)
                    )
                ).start()
            except ValueError:
                messagebox.showerror("Error", "Invalid time format! Use HH:MM")
        else:
            messagebox.showerror("Error", "Invalid folder path!")

    def run_big_post(subs_path):
        proxy, message = get_proxy(reddit_account_email)
        if proxy is None:
            messagebox.showerror("Error", message)
        else:
            big_post(
                subs_path,
                reddit_account_email,
                reddit_account_password,
                **proxy
            )
        messagebox.showinfo("Success", "Posting started!")

    root = tk.Tk()
    root.title("Reddit Big Poster")

    tk.Label(root, text="Select Account:", font=("Modern No. 20", 18)).grid(
        row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Choose Account", font=("Modern No. 20", 18), command=lambda: choose_email_window(
        update_status)).grid(row=0, column=1, padx=10, pady=10)
    label_selected_account = tk.Label(
        root, text="No account selected", font=("Modern No. 20", 18), fg="red")
    label_selected_account.grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Select subs folder:", font=("Modern No. 20", 18)).grid(
        row=1, column=0, padx=10, pady=10)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", font=("Modern No. 20", 18), command=select_folder).grid(
        row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Start Time (HH:MM):", font=("Modern No. 20", 18)).grid(
        row=2, column=0, padx=10, pady=10)
    entry_time = tk.Entry(root, width=10)
    entry_time.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Start Posting", font=("Modern No. 20", 18), command=start_big_post).grid(
        row=3, column=1, padx=10, pady=10)

    root.mainloop()
