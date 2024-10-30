import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import random
import os

from log_windows import init_log_window, log_message


def uniq_tkinter():
    def uniqueize_video(file_path):
        log_message(f"Starting video uniqueization for: {file_path}")
        status_label.config(text="Uniqueizing video...")
        base_name, ext = os.path.splitext(file_path)
        output_file = f"{base_name}_uniq{ext}"
        angle = random.randint(-3, 3)
        crop_pixels = random.randint(1, 7)

        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            messagebox.showerror("Video", "Failed to open video.")
            log_message("Error: Failed to open video.")
            status_label.config(text="Ready")
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        ret, frame = cap.read()
        if not ret:
            cap.release()
            messagebox.showerror("Video", "Failed to read video frame.")
            log_message("Error: Failed to read video frame.")
            status_label.config(text="Ready")
            return

        (h, w) = frame.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(frame, M, (w, h))
        cropped = rotated[crop_pixels:h - crop_pixels, crop_pixels:w - crop_pixels]

        new_height, new_width = cropped.shape[:2]
        out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for _ in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            rotated = cv2.warpAffine(frame, M, (w, h))
            cropped = rotated[crop_pixels:h - crop_pixels, crop_pixels:w - crop_pixels]
            out.write(cropped)

        cap.release()
        out.release()

        messagebox.showinfo("Video", f"Video uniqueization completed! Angle: {angle}°, Crop: {crop_pixels}px")
        log_message(f"Video uniqueization completed for {file_path}. Output: {output_file}")
        status_label.config(text="Ready")

        return output_file

    def uniqueize_photo(file_path):
        log_message(f"Starting photo uniqueization for: {file_path}")
        base_name, ext = os.path.splitext(file_path)
        output_file = f"{base_name}_uniq{ext}"

        angle = random.randint(-2, 2)
        crop_pixels = random.randint(1, 7)

        image = cv2.imread(file_path)
        if image is None:
            log_message("Error: Failed to open image.")
            raise FileNotFoundError("Failed to open image.")

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))

        cropped = rotated[crop_pixels:h - crop_pixels, crop_pixels:w - crop_pixels]
        cv2.imwrite(output_file, cropped)

        log_message(f"Photo uniqueization completed for {file_path}. Output: {output_file}")
        return output_file

    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, file_path)
            log_message(f"Selected file: {file_path}")

    def start_uniqueization():
        selected_function = function_var.get()
        file_path = entry_file.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a file")
            log_message("Error: No file selected.")
            return

        valid_video_extensions = {".mp4", ".avi", ".mov"}
        valid_photo_extensions = {".jpg", ".jpeg", ".png"}

        file_extension = file_path.split(".")[-1].lower()

        if selected_function == "Video":
            if f".{file_extension}" not in valid_video_extensions:
                messagebox.showerror("Error", "Please select a valid video file")
                log_message("Error: Invalid video file extension.")
                return
            uniqueize_video(file_path)

        elif selected_function == "Photo":
            if f".{file_extension}" not in valid_photo_extensions:
                messagebox.showerror("Error", "Please select a valid photo file")
                log_message("Error: Invalid photo file extension.")
                return
            uniqueize_photo(file_path)

        else:
            messagebox.showerror("Error", "Please select a function")
            log_message("Error: No uniqueization function selected.")

    root = tk.Tk()
    root.title("Uniqueizer")

    tk.Label(root, text="Select file:").grid(row=0, column=0, padx=10, pady=10)
    entry_file = tk.Entry(root, width=50)
    entry_file.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

    function_var = tk.StringVar(value="Video")
    tk.Radiobutton(root, text="Uniqueize Video", variable=function_var, value="Video").grid(row=1, column=0, padx=10,
                                                                                            pady=5)
    tk.Radiobutton(root, text="Uniqueize Photo", variable=function_var, value="Photo").grid(row=1, column=1, padx=10,
                                                                                            pady=5)

    tk.Button(root, text="Start", command=start_uniqueization).grid(row=2, column=0, columnspan=3, pady=10)
    status_label = tk.Label(root, text="Ready")
    status_label.grid(row=3, column=0, columnspan=3, pady=10)

    init_log_window()
    root.mainloop()

uniq_tkinter()