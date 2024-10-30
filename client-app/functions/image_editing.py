import tkinter as tk
from tkinter import filedialog, messagebox


def uniqueize_video():
    status_label.config(text="Uniqueizing video...")
    # Placeholder for video uniqueization code
    messagebox.showinfo("Video", "Video uniqueization completed!")
    status_label.config(text="Ready")


def uniqueize_photo():
    status_label.config(text="Uniqueizing photo...")
    # Placeholder for photo uniqueization code
    messagebox.showinfo("Photo", "Photo uniqueization completed!")
    status_label.config(text="Ready")


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

    # Check file extension based on selection
    valid_video_extensions = {".mp4", ".avi", ".mov"}
    valid_photo_extensions = {".jpg", ".jpeg", ".png"}

    file_extension = file_path.split(".")[-1].lower()

    if selected_function == "Video":
        if f".{file_extension}" not in valid_video_extensions:
            messagebox.showerror("Error", "Please select a valid video file")
            return
        uniqueize_video()

    elif selected_function == "Photo":
        if f".{file_extension}" not in valid_photo_extensions:
            messagebox.showerror("Error", "Please select a valid photo file")
            return
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

status_label = tk.Label(root, text="Ready")
status_label.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
