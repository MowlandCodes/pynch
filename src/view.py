from customtkinter import (CTk, CTkButton, CTkFrame, CTkImage, CTkLabel,
                           set_appearance_mode, set_default_color_theme)
from PIL import Image

set_appearance_mode("System")
set_default_color_theme("src/theme/breeze.json")


class TitleBar(CTkFrame):
    def __init__(self, parent: CTk, icon_path: str):
        self.parent = parent
        self.icon_path = icon_path
        super().__init__(self.parent, fg_color="transparent", corner_radius=0)

        # Configure grid for Title Bar
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title Label
        self.app_icon = self.load_icon(self.icon_path, (24, 24))
        self.title_lable = CTkLabel(
            self,
            text="Pynch",
            image=self.app_icon,
            compound="left",
            font=("Roboto", 14, "bold"),
            padx=10,
            pady=12,
        )

        self.title_lable.grid(row=0, column=1, sticky="w")

        # Control Frame
        self.control_frame = CTkFrame(self.parent, fg_color="transparent")
        self.control_frame.grid(row=0, column=2, sticky="e", padx=5)

        # Icon
        self.minimize_icon = self.load_icon("src/icons/minimize.png", (24, 24))
        self.maximize_icon = self.load_icon("src/icons/maximize.png", (24, 24))
        self.close_icon = self.load_icon("src/icons/close.png", (24, 24))

        CTkButton(
            self.control_frame,
            text="",
            image=self.minimize_icon,
            fg_color="transparent",
            width=30,
            height=30,
        ).pack(side="left")

    def load_icon(self, path, size):
        self.path = path
        self.size = size
        return CTkImage(Image.open(self.path), size=self.size)


class MainView(CTk):
    def __init__(self):
        super().__init__()
        self.title("Pynch")
        self.resizable(True, True)

        self.overrideredirect(True)

        self.width = 1250
        self.height = 650
        self.mid_width = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.mid_height = (self.winfo_screenheight() // 2) - (self.height // 2)

        self.geometry(f"{self.width}x{self.height}+{self.mid_width}+{self.mid_height}")

        # Configure Main Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add Custom Title Bar
        self.title_bar = TitleBar(self, icon_path="src/icons/app_icon.png")
        self.title_bar.grid(row=0, column=0, sticky="ew")

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
