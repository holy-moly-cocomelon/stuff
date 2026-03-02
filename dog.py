import time
import sys
import os
import threading
import simpleaudio as sa
from PIL import Image, ImageTk
import tkinter as tk

DURATION = 15  # seconds

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp dir
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def play_audio():
    audio_path = resource_path("sound.wav")
    wave = sa.WaveObject.from_wave_file(audio_path)
    play = wave.play()
    time.sleep(DURATION)
    play.stop()

def show_image():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.overrideredirect(True)

    img = Image.open(resource_path("image.png"))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.pack()

    # center window
    w, h = img.size
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.after(DURATION * 1000, root.destroy)
    root.mainloop()

# Run audio + image together
threading.Thread(target=play_audio, daemon=True).start()
show_image()
