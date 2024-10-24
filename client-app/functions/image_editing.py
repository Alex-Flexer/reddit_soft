import tkinter as tk
from tkinter import filedialog, messagebox


def uniqueize_video():
    # Заглушка для уникализации видео
    messagebox.showinfo("Video", "Video uniqueization started!")


def uniqueize_photo():
    # Заглушка для уникализации фото
    messagebox.showinfo("Photo", "Photo uniqueization started!")


def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)


def start_uniqueization():
    selected_function = function_var.get()
    file_path = entry_file.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a file")
        return

    if selected_function == "Video":
        uniqueize_video()
    elif selected_function == "Photo":
        uniqueize_photo()
    else:
        messagebox.showerror("Error", "Please select a function")


root = tk.Tk()
root.title("Uniqueizer")

tk.Label(root, text="Select file:").grid(row=0, column=0, padx=10, pady=10)
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

function_var = tk.StringVar(value="Video")
tk.Radiobutton(root, text="Uniqueize Video", variable=function_var, value="Video").grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Uniqueize Photo", variable=function_var, value="Photo").grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Start", command=start_uniqueization).grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
