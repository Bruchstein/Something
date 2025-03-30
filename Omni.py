import tkinter as tk
import os
import requests
import tempfile
import screeninfo
import pygame
from PIL import Image, ImageTk
import time

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.milliseconds = [
            5300, 8460, 11670, 14870,
            18060, 21260, 24470, 27620,
            30800, 33950, 37150
        ]
        self.configure(bg='black')  # Ensure background starts as black
        self.attributes('-fullscreen', True)
        
        self.thiccc = tk.Label(self, bg='black')
        self.thiccc.pack(fill=tk.BOTH, expand=True)
        
        self.volume = 0.2  # Volume level (0.0 to 1.0)
        self.setup()
    
    def setup(self):
        temp_folder = self.create_temp_folder()
        self.download_files(temp_folder)
        self.image_path = self.get_image_path(temp_folder)
        self.play_audio(os.path.join(temp_folder, "hotmilk.mp3"))
    
    def create_temp_folder(self):
        """Creates a temporary folder and returns its path."""
        temp_dir = os.path.join(tempfile.gettempdir(), "ThiccOmniMan")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def download_files(self, folder_path):
        """Downloads files based on the user's screen resolution."""
        download_links = {
            "2560x1440": {"url": "https://raw.githubusercontent.com/Bruchstein/Something/main/OmniMan/thiccomniman_2560x1440.png", "file_name": "Thicc_2560x1440.png"},
            "1920x1080": {"url": "https://raw.githubusercontent.com/Bruchstein/Something/main/OmniMan/thiccomniman_1920x1080.png", "file_name": "Thicc_1920x1080.png"},
            "mp3": {"url": "https://raw.githubusercontent.com/Bruchstein/Something/main/OmniMan/hotmilk.mp3", "file_name": "hotmilk.mp3"}
        }
        
        screen = screeninfo.get_monitors()[0]
        resolution_key = "2560x1440" if (screen.width, screen.height) == (2560, 1440) else "1920x1080"
        selected_files = [download_links[resolution_key], download_links["mp3"]]

        for file in selected_files:
            file_path = os.path.join(folder_path, file["file_name"])
            if not os.path.exists(file_path):
                try:
                    response = requests.get(file["url"], stream=True)
                    response.raise_for_status()
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {file_path}")
                except requests.RequestException as e:
                    print(f"Failed to download {file['url']}: {e}")
                    input("")
    
    def get_image_path(self, folder_path):
        """Returns the correct image path based on resolution."""
        screen = screeninfo.get_monitors()[0]
        resolution_key = "2560x1440" if (screen.width, screen.height) == (2560, 1440) else "1920x1080"
        return os.path.join(folder_path, f"Thicc_{resolution_key}.png")

    def play_audio(self, file_path):
        """Plays the audio file and schedules image display events."""
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

        for time_stamp in self.milliseconds:
            self.after(time_stamp, self.show_image)
            self.after(time_stamp + 860, self.hide_image)

        # Check if the music has finished and close after 2 seconds
        self.after(2000, self.check_music_end)

    def check_music_end(self):
        """Checks if the music is still playing, then closes the program."""
        if not pygame.mixer.music.get_busy():
            self.quit()  # Close the program after 2 seconds when music finishes
        else:
            self.after(1000, self.check_music_end)  # Check again after 1 second

    def show_image(self):
        """Displays the downloaded image as fullscreen background."""
        image = Image.open(self.image_path)
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)
        self.thiccc.configure(image=self.bg_image, bg='black')
        self.thiccc.image = self.bg_image
    
    def hide_image(self):
        """Hides the image by making the background black again."""
        self.thiccc.configure(image='', bg='black')

if __name__ == "__main__":
    app = MainForm()
    app.mainloop()
