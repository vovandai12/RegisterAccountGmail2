import tkinter as tk
from file_paths import FilePaths


class FormatFrame(tk.Toplevel):
    def __init__(self, cnf={}, **kwargs):
        tk.Toplevel.__init__(self, **kwargs, bg="white")
        self.size = [600, 300]
        self.title(f"Tool tạo tài khoản gmail - Liên hệ telegram @ttruong27758")
        self.geometry("{}x{}".format(self.size[0], self.size[1]))
        self.resizable(0, 0)
        self.iconbitmap(FilePaths.ICON_MAIN.value)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - self.size[0] / 2)
        center_y = int(screen_height / 2 - self.size[1] / 2)
        self.geometry(f"{self.size[0]}x{self.size[1]}+{center_x}+{center_y}")
