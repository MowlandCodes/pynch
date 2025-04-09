from customtkinter import *
from PIL import Image, ImageTk

from src import *

set_appearance_mode("System")
set_default_color_theme("src/themes/NightTrain.json")


class MainView(CTk):
    def __init__(self):
        super().__init__()
        self.title("Pynch")
        self.after(200, lambda: self.wm_iconphoto(True, self.app_icon))
        self.resizable(True, True)

        self.app_icon = ImageTk.PhotoImage(
            Image.open(f"{ICON_PATH}app_icon.png"), size=(48, 48)
        )
        self.is_maximized = False
        self.is_minimized = False
        self.original_geometry = None

        self.width = 1250
        self.height = 650
        self.mid_width = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.mid_height = (self.winfo_screenheight() // 2) - (self.height // 2)

        self.geometry(f"{self.width}x{self.height}+{self.mid_width}+{self.mid_height}")

        self.configure_layout()
        self.set_app_widgets()

    def configure_layout(self):
        # Configure Main Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main Container Frame
        self.main_container = CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar = CTkFrame(self.main_container, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # Main Content Frame
        self.main_content = CTkFrame(self.main_container, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

    def set_app_widgets(self):
        pass
