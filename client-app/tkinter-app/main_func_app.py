import tkinter as tk
from image_editing import uniqueize_photo, uniqueize_video
from registration import registration
from converters import tkinter_converters
from posting import post_mech
from big_post import tkinter_reddit_big_post
from farm_carma import tkinter_karma_farm


def create_window():
    root = tk.Tk()
    root.title("Reddit Soft")

    root.geometry("400x400")

    root.configure(bg="#f0f0f0")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    button_config = {
        "font": ("Arial", 14, "bold"),
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "activeforeground": "black",
        "bd": 3,
        "relief": "raised",
        "width": 28,
        "height": 2
    }

    label = tk.Label(scrollable_frame, text="Choose a Function", font=("Arial", 18), bg="#f0f0f0")
    label.pack(pady=10)

    buttons = [
        ("Uniqueize Video", uniqueize_video),
        ("Uniqueize Photo", uniqueize_photo),
        ("Registration", registration),
        ("Farm Karma", tkinter_karma_farm),
        ("Post Auto", tkinter_reddit_big_post),
        ("post_mech", post_mech),
        ("converters", tkinter_converters)
    ]

    for (text, func) in buttons:
        button = tk.Button(scrollable_frame, text=text, command=func, **button_config)
        button.pack(pady=10)

    root.mainloop()


