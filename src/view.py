from customtkinter import (CTk, CTkButton, CTkFrame, set_appearance_mode,
                           set_default_color_theme)

set_appearance_mode("System")
set_default_color_theme("src/theme/breeze.json")


class MainView(CTk):
    def __init__(self):
        super().__init__()
        self.title("Pynch Password Manager")
        self.resizable(True, True)

        self.width = 1250
        self.height = 650
        self.mid_width = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.mid_height = (self.winfo_screenheight() // 2) - (self.height // 2)

        self.geometry(f"{self.width}x{self.height}+{self.mid_width}+{self.mid_height}")
