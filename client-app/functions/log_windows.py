import tkinter as tk
from tkinter import scrolledtext

# Глобальное окно для логов
log_window = None


def init_log_window():
    global log_window, log_text
    log_window = tk.Toplevel()
    log_window.title("Log Output")
    log_window.geometry("400x300")

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=50, height=15)
    log_text.pack(pady=10, padx=10)
    log_text.insert(tk.END, "Log output:\n")


def log_message(message: str):
    if log_window is None or not log_window.winfo_exists():
        init_log_window()
    log_text.insert(tk.END, f"{message}\n")
    log_text.see(tk.END)  # Автоматическая прокрутка вниз
    log_window.update_idletasks()
