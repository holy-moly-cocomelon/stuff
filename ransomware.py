import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk
import vlc
import random

IMAGE_URL = "https://raw.githubusercontent.com/holy-moly-cocomelon/image/refs/heads/main/hahaha.png"
AUDIO_URL = "https://raw.githubusercontent.com/holy-moly-cocomelon/image/refs/heads/main/respect.mp4"
BTC_ADDRESS = "1362317df7126fg1h2183736461hfdhfyw7274"


class FakeRansomware:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YOUR COMPUTER IS LOCKED")
        # ---- FULLSCREEN LOCK (as original) ----
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        self.root.configure(bg="#8B0000")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")

        # Secret clean exit
        self.root.bind("<Control-Shift-Q>", lambda e: self.root.destroy())

        self.haha_pil = None
        self.bounce_photo = None
        self.bouncers = []
        self.player = None

        self.create_widgets()           # ← your original scary screen
        self.start_audio()
        self.start_fake_countdown()

        # Troll mode exactly after 30 seconds
        self.root.after(30000, self.switch_to_troll_mode)

        self.root.mainloop()

    def load_image(self):
        if self.haha_pil:
            return True
        try:
            r = requests.get(IMAGE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            self.haha_pil = Image.open(BytesIO(r.content))
            return True
        except:
            return False

    def create_widgets(self):
        # ────────────────────────────────────────────────
        # Your original scary layout — unchanged
        # ────────────────────────────────────────────────
        main = tk.Frame(self.root, bg="#8B0000")
        main.pack(expand=True, fill="both", padx=60, pady=40)

        # ---- IMAGE (STATIC PLACEHOLDER) ----
        if self.load_image():
            img = self.haha_pil.copy()
            img.thumbnail((500, 500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(main, image=photo, bg="#8B0000")
            lbl.image = photo
            lbl.pack(side="left", padx=40)
        else:
            tk.Label(
                main,
                text="IMAGE FAILED TO LOAD",
                font=("Courier", 18, "bold"),
                fg="yellow",
                bg="#8B0000"
            ).pack(side="left", padx=40)

        # ---- TEXT ----
        text = tk.Frame(main, bg="#8B0000")
        text.pack(side="left", fill="y")
        tk.Label(
            text,
            text="YOUR FILES HAVE BEEN ENCRYPTED!",
            font=("Courier", 44, "bold"),
            fg="#FF0000",
            bg="#8B0000"
        ).pack(pady=20)
        self.timer_label = tk.Label(
            text,
            text="48:00:00",
            font=("Courier", 48, "bold"),
            fg="#FFFF00",
            bg="#8B0000"
        )
        self.timer_label.pack(pady=20)
        tk.Label(
            text,
            text=f"Send 0.15 BTC to:\n{BTC_ADDRESS}",
            font=("Courier", 20, "bold"),
            fg="white",
            bg="black",
            padx=20,
            pady=10
        ).pack(pady=30)

    def start_fake_countdown(self):
        self.seconds_left = 48 * 3600
        self.update_timer()

    def update_timer(self):
        if self.seconds_left <= 0:
            self.timer_label.config(text="TIME IS UP", fg="red")
            return
        h = self.seconds_left // 3600
        m = (self.seconds_left % 3600) // 60
        s = self.seconds_left % 60
        self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.seconds_left -= 1
        self.root.after(1000, self.update_timer)

    def start_audio(self):
        try:
            self.vlc_instance = vlc.Instance("--no-video", "--quiet")
            self.player = self.vlc_instance.media_player_new()
            media = self.vlc_instance.media_new(AUDIO_URL)
            media.add_option("input-repeat=-1")
            self.player.set_media(media)
            self.player.audio_set_volume(100)
            self.root.after(100, self.player.play)
        except:
            pass

    def mute_audio(self, muted):
        try:
            if self.player:
                self.player.audio_set_mute(muted)
        except:
            pass

    def switch_to_troll_mode(self):
        # Clear scary screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="black")
        try:
            self.root.attributes("-transparentcolor", "black")
        except:
            pass  # some OS ignore this

        # Prepare smaller bouncing version
        if self.load_image():
            img = self.haha_pil.copy()
            img.thumbnail((280, 280), Image.Resampling.LANCZOS)
            self.bounce_photo = ImageTk.PhotoImage(img)

        # Start with 3 demons
        for _ in range(3):
            self.spawn_bouncer()

        self.bounce_loop()

        # Audio drama: wait 5s → mute 5s → unmute forever
        self.root.after(5000, lambda: self.mute_audio(True))
        self.root.after(10000, lambda: self.mute_audio(False))

    def spawn_bouncer(self):
        if not self.bounce_photo:
            return

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        iw, ih = self.bounce_photo.width(), self.bounce_photo.height()

        x = random.randint(20, sw - iw - 20)
        y = random.randint(20, sh - ih - 20)

        lbl = tk.Label(self.root, image=self.bounce_photo, bg="black", bd=0)
        lbl.place(x=x, y=y)

        vx = random.choice([-16, -14, -12, 12, 14, 16])
        vy = random.choice([-16, -14, -12, 12, 14, 16])

        self.bouncers.append({
            'label': lbl,
            'x': float(x), 'y': float(y),
            'vx': vx, 'vy': vy,
            'w': iw, 'h': ih
        })

    def bounce_loop(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        for b in self.bouncers[:]:  # copy to allow adding during loop
            b['x'] += b['vx']
            b['y'] += b['vy']

            hit_edge = False
            hit_corner = False

            if b['x'] <= 0 or b['x'] + b['w'] >= sw:
                b['vx'] *= -1
                b['x'] = max(0, min(sw - b['w'], b['x']))
                hit_edge = True

            if b['y'] <= 0 or b['y'] + b['h'] >= sh:
                b['vy'] *= -1
                b['y'] = max(0, min(sh - b['h'], b['y']))
                hit_edge = True

            if (b['x'] <= 0 or b['x'] + b['w'] >= sw) and \
               (b['y'] <= 0 or b['y'] + b['h'] >= sh):
                hit_corner = True

            b['label'].place(x=int(b['x']), y=int(b['y']))

            if hit_edge:
                self.trigger_scary()
                if hit_corner:
                    self.trigger_scary()   # extra scary on corner
                    self.spawn_bouncer()   # duplicate

        self.root.after(20, self.bounce_loop)

    def trigger_scary(self):
        # Red flash
        flash = tk.Label(self.root, bg="#FF0000", bd=0)
        flash.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.after(120, flash.destroy)

        # Big warning text
        txt = tk.Label(self.root,
                       text="😈 IT'S GETTING WORSE!",
                       font=("Courier", 80, "bold"),
                       fg="yellow", bg="#FF0000",
                       padx=40, pady=20)
        txt.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(350, txt.destroy)

        # Spawn even more demons sometimes
        if random.random() < 0.4:
            self.spawn_bouncer()


if __name__ == "__main__":
    FakeRansomware()
