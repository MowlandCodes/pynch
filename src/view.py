import threading

import pystray
from customtkinter import (CTk, CTkButton, CTkFrame, CTkImage, CTkLabel,
                           set_appearance_mode, set_default_color_theme)
from PIL import Image

from src import *

set_appearance_mode("System")
set_default_color_theme("src/themes/NightTrain.json")


class TitleBar(CTkFrame):
    def __init__(self, parent: CTk, app_icon: str):
        self.parent = parent
        self.icon = app_icon

        super().__init__(self.parent, fg_color="transparent", corner_radius=0)

        # Configure grid for Title Bar
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Icon
        self.app_icon = self.load_icon(f"{ICON_PATH}{self.icon}", (24, 24))
        self.minimize_icon = self.load_icon(f"{ICON_PATH}minimize.png", (24, 24))
        self.maximize_icon = self.load_icon(f"{ICON_PATH}maximize.png", (24, 24))
        self.close_icon = self.load_icon(f"{ICON_PATH}close.png", (24, 24))
        self.restore_icon = self.load_icon(f"{ICON_PATH}restore.png", (24, 24))

        self.set_title_bar()
        self.bind_drag_title()

    def set_title_bar(self):
        # Title Label
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

        # Window Control Buttons
        self.minimize_btn = CTkButton(
            self.control_frame,
            text="",
            image=self.minimize_icon,
            fg_color="transparent",
            width=30,
            height=30,
            command=self.animate_minimize,
        )
        self.minimize_btn.pack(side="left", padx=5)  # Minimize Button

        self.maximize_btn = CTkButton(
            self.control_frame,
            text="",
            image=self.maximize_icon,
            fg_color="transparent",
            width=30,
            height=30,
            command=self.toggle_maximize,
        )
        self.maximize_btn.pack(side="left", padx=5)  # Maximize Button

        self.close_btn = CTkButton(
            self.control_frame,
            text="",
            image=self.close_icon,
            fg_color="transparent",
            width=30,
            height=30,
            command=self.close,
        )
        self.close_btn.pack(side="left", padx=5)  # Close Icon

    def animate_minimize(self):
        if self.parent.is_minimized:
            return

        self.parent.is_minimized = True
        self.parent.original_geometry = self.parent.geometry()

        # Get current dimensions and position
        current_width = self.parent.winfo_width()
        current_height = self.parent.winfo_height()
        current_x = self.parent.winfo_x()
        current_y = self.parent.winfo_y()

        # Target dimensions (bottom-right corner)
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        target_width = 100
        target_height = 50
        target_x = screen_width - target_width - 10
        target_y = 30

        # Animation parameters
        steps = 20
        duration = 300  # milliseconds

        delta_width = (target_width - current_width) / steps
        delta_height = (target_height - current_height) / steps
        delta_x = (target_x - current_x) / steps
        delta_y = (target_y - current_y) / steps

        # Animation loop
        for step in range(1, steps + 1):
            new_width = int(current_width + delta_width * step)
            new_height = int(current_height + delta_height * step)
            new_x = int(current_x + delta_x * step)
            new_y = int(current_y + delta_y * step)

            self.parent.after(
                int(duration * step / steps),
                lambda w=new_width, h=new_height, x=new_x, y=new_y: self.parent.geometry(
                    f"{w}x{h}+{x}+{y}"
                ),
            )

        # After animation, hide window and show tray icon
        self.parent.after(duration, self.show_tray_icon)

    def show_tray_icon(self):
        # Create system tray icon
        image = Image.open(f"{ICON_PATH}app_icon.png")
        menu = pystray.Menu(
            pystray.MenuItem("Restore Pynch", self.restore_window, default=True)
        )
        self.parent.tray_icon = pystray.Icon(
            "Pynch", image, "Pynch", menu, visible=True
        )

        # Run the tray icon in a separate thread
        self.tray_thread = threading.Thread(
            target=self.parent.tray_icon.run, daemon=True
        )
        self.tray_thread.start()
        self.parent.withdraw()  # Hide main window

    def restore_window(self, icon=None, item=None):
        if hasattr(self.parent, "tray_icon"):
            self.parent.tray_icon.stop()
            self.parent.is_minimized = False

            self.parent.after(0, self.parent.deiconify)
            self.parent.after(0, self.parent.lift)
            self.parent.after(0, self.parent.focus_force)

            self.parent.after(100, self.animate_restore_tray)

    def animate_restore_tray(self):
        # Get original geometry
        geom = self.parent.original_geometry.split("+")
        original_width, original_height = map(int, geom[0].split("x"))
        original_x = int(geom[1])
        original_y = int(geom[2])

        # Current dimensions (from minimized state)
        current_width = self.parent.winfo_width()
        current_height = self.parent.winfo_height()
        current_x = self.parent.winfo_x()
        current_y = self.parent.winfo_y()

        # Animation parameters
        steps = 20
        duration = 300  # milliseconds

        delta_width = (original_width - current_width) / steps
        delta_height = (original_height - current_height) / steps
        delta_x = (original_x - current_x) / steps
        delta_y = (original_y - current_y) / steps

        # Animation loop
        for step in range(1, steps + 1):
            new_width = int(current_width + delta_width * step)
            new_height = int(current_height + delta_height * step)
            new_x = int(current_x + delta_x * step)
            new_y = int(current_y + delta_y * step)

            self.parent.after(
                int(duration * step / steps),
                lambda w=new_width, h=new_height, x=new_x, y=new_y: self.parent.geometry(
                    f"{w}x{h}+{x}+{y}"
                ),
            )

        # Show window after animation
        self.parent.after(duration, self.parent.deiconify)

    def animate_maximize(self):
        if self.parent.is_maximized:
            return

        self.parent.is_maximized = True
        self.maximize_btn.configure(image=self.restore_icon)

        # Save current geometry
        self.parent.original_geometry = self.parent.geometry()

        # Get target dimensions
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # Get current dimensions
        current_width = self.parent.winfo_width()
        current_height = self.parent.winfo_height()
        current_x = self.parent.winfo_x()
        current_y = self.parent.winfo_y()

        # Animation parameters
        steps = 20
        duration = 200  # milliseconds
        delta_width = (screen_width - current_width) / steps
        delta_height = (screen_height - current_height) / steps
        delta_x = (0 - current_x) / steps
        delta_y = (0 - current_y) / steps

        # Animation loop
        for step in range(1, steps + 1):
            new_width = int(current_width + delta_width * step)
            new_height = int(current_height + delta_height * step)
            new_x = int(current_x + delta_x * step)
            new_y = int(current_y + delta_y * step)

            self.parent.after(
                int(duration * step / steps),
                lambda w=new_width, h=new_height, x=new_x, y=new_y: self.parent.geometry(
                    f"{w}x{h}+{x}+{y}"
                ),
            )

    def animate_restore_maximize(self):
        if not self.parent.is_maximized:
            return

        self.parent.is_maximized = False
        self.maximize_btn.configure(image=self.maximize_icon)

        # Get original geometry
        geom = self.parent.original_geometry.split("+")
        size = geom[0].split("x")
        original_width = int(size[0])
        original_height = int(size[1])
        original_x = int(geom[1])
        original_y = int(geom[2])

        # Current dimensions
        current_width = self.parent.winfo_width()
        current_height = self.parent.winfo_height()
        current_x = self.parent.winfo_x()
        current_y = self.parent.winfo_y()

        # Animation parameters
        steps = 20
        duration = 200  # milliseconds
        delta_width = (original_width - current_width) / steps
        delta_height = (original_height - current_height) / steps
        delta_x = (original_x - current_x) / steps
        delta_y = (original_y - current_y) / steps

        # Animation loop
        for step in range(1, steps + 1):
            new_width = int(current_width + delta_width * step)
            new_height = int(current_height + delta_height * step)
            new_x = int(current_x + delta_x * step)
            new_y = int(current_y + delta_y * step)

            self.parent.after(
                int(duration * step / steps),
                lambda w=new_width, h=new_height, x=new_x, y=new_y: self.parent.geometry(
                    f"{w}x{h}+{x}+{y}"
                ),
            )

    def toggle_maximize(self):
        return (
            self.animate_maximize()
            if self.parent.is_maximized == False
            else self.animate_restore_maximize()
        )

    def close(self):
        if hasattr(self.parent, "tray_icon"):
            self.parent.tray_icon.stop()
        self.parent.destroy()

    def load_icon(self, path, size):
        self.path = path
        self.size = size
        return CTkImage(Image.open(self.path), size=self.size)

    def bind_drag_title(self):
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.dragging)

    def start_drag(self, event):
        self.pos_x, self.pos_y = event.x, event.y

    def dragging(self, event):
        if not self.parent.is_maximized:
            x = self.parent.winfo_x() + (
                event.x_root - self.pos_x - self.parent.winfo_rootx()
            )
            y = self.parent.winfo_y() + (
                event.y_root - self.pos_y - self.parent.winfo_rooty()
            )
            self.parent.geometry(f"+{x}+{y}")


class MainView(CTk):
    def __init__(self):
        super().__init__()
        self.title("Pynch")
        self.resizable(True, True)

        self.is_maximized = False
        self.is_minimized = False
        self.original_geometry = None

        self.attributes("-type", "splash")

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

        # Add Custom Title Bar
        self.title_bar = TitleBar(self, app_icon="app_icon.png")
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
