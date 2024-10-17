from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading

def download_reals(url):
    pass


def download_shorts(url):
    try:
        video = YouTube(url)
        stream = video.streams.filter(file_extension='mp4', only_video=True).first()
        if stream is not None:
            stream.download()
            print("Download complete.")
        else:
            print("No compatible video found.")
    except Exception as e:
        print("An error occurred during download:", str(e))


def download_tiktok(url):
    pass
