import tkinter as tk
from tkinter import scrolledtext

from tkinter.scrolledtext import ScrolledText

# Глобальное окно для логов
class LogWindow:
    _log_window: tk.Toplevel
    _log_text: ScrolledText

    def __init__(self):
        self.log_window = tk.Toplevel()
        self.log_window.title("Log Output")
        self.log_window.geometry("400x300")

        self._log_text = scrolledtext.ScrolledText(self.log_window, wrap=tk.WORD, width=50, height=15)
        self._log_text.pack(pady=10, padx=10)
        self._log_text.insert(tk.END, "Log output:\n")

    def log_message(self, *messages: str, sep: str=' ', end: str='\n'):
        message = sep.join(messages) + end
        self._log_text.insert(tk.END, f"{message}\n")
        self._log_text.see(tk.END)  # Автоматическая прокрутка вниз
        self.log_window.update_idletasks()
