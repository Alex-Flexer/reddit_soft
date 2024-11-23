from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from requests import post
from json import dumps
from os.path import join, exists
from zipfile import ZipFile


def download_software(username: str, password: str, folder_path: str) -> str | None:
    data = dumps({"email": username, "password": password})
    resp = post("http://reddsyndicate.com/get/software", data=data)

    if resp.status_code != 200 or not exists(folder_path):
        return None

    download_path = join(folder_path, "software.zip")
    with open(download_path, "wb") as f:
        f.write(resp.content)
    return download_path


def extract_zip(zip_path: str, extract_to: str):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def login_window():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        data = dumps({"email": username, "password": password})
        resp = post("http://reddsyndicate.com/get/software", data=data)

        if resp.status_code == 200:
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
            file_selection_window(username, password)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    root = Tk()
    root.title("Login")
    root.geometry("300x200")

    Label(root, text="Telegram Username:").pack(pady=5)
    username_entry = Entry(root, width=30)
    username_entry.pack(pady=5)

    Label(root, text="Password:").pack(pady=5)
    password_entry = Entry(root, width=30, show="*")
    password_entry.pack(pady=5)

    submit_button = Button(root, text="Login", command=validate_login)
    submit_button.pack(pady=10)

    root.mainloop()


def file_selection_window(username: str, password: str):
    def download_and_extract():
        folder_path = filedialog.askdirectory(title="Select folder for download")
        if not folder_path:
            messagebox.showerror("Error", "No folder selected!")
            return

        messagebox.showinfo("Information", "Download started. Please wait...")
        zip_path = download_software(username, password, folder_path)
        if not zip_path:
            messagebox.showerror("Error", "Failed to download file! Check your connection.")
            return

        try:
            extract_zip(zip_path, folder_path)
            messagebox.showinfo("Success", f"Archive successfully extracted to {folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract archive: {str(e)}")

    root = Tk()
    root.title("Folder Selection")
    root.geometry("300x150")

    Label(root, text="Select folder for downloading and extracting the file").pack(pady=10)

    download_button = Button(root, text="Select Folder", command=download_and_extract)
    download_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    login_window()
