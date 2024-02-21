import tkinter as tk
from tkinter import messagebox
from file_paths import FilePaths
from views.home_frame import HomeFrame
from views.setting_frame import SettingFrame
from views.bottom_frame import BottomFrame
from config import LoadConfig
import config as config


class MainWindow:
    def __init__(self):
        config.global_config = LoadConfig()
        self.window = tk.Tk()
        self.window.config(bg="white")
        self.size = [1200, 600]
        self.window.title(f"Tool tạo tài khoản gmail - Liên hệ telegram @ttruong27758")
        self.window.geometry("{}x{}".format(self.size[0], self.size[1]))
        self.window.resizable(0, 0)
        self.window.iconbitmap(FilePaths.ICON_MAIN.value)
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width / 2 - self.size[0] / 2)
        center_y = int(screen_height / 2 - self.size[1] / 2)
        self.window.geometry(f"{self.size[0]}x{self.size[1]}+{center_x}+{center_y}")
        frame_home = HomeFrame(
            self.window, width=int(self.size[0] * 0.6), height=self.size[1] - 50
        )
        frame_setting = SettingFrame(
            self.window, width=int(self.size[0] * 0.4), height=self.size[1] - 50
        )
        frame_bottom = BottomFrame(self.window, width=self.size[0], height=50)

        frame_home.grid(row=0, column=0, sticky=tk.NSEW)
        frame_setting.grid(row=0, column=1, sticky=tk.NSEW)
        frame_bottom.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

    def run(self):
        self.window.mainloop()

    def on_close(self):
        response = messagebox.askyesno("Exit", "Bạn có muốn thoát chương trình ?")
        if response:
            self.window.destroy()
