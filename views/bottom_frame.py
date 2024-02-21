import tkinter as tk


class BottomFrame(tk.Frame):
    def __init__(self, window, cnf={}, **kwargs):
        tk.Frame.__init__(self, window, **kwargs, bg="white")
        label_error = tk.Label(self, text="Thất bại: ", fg="red", bg="white")
        self.label_total_error = tk.Label(self, text="0", fg="red", bg="white")
        label_success = tk.Label(self, text="Thành công: ", fg="green", bg="white")
        self.label_total_success = tk.Label(self, text="0", fg="green", bg="white")
        label_time = tk.Label(self, text="Thời gian còn lại: ", fg="green", bg="white")
        self.label_time_re = tk.Label(self, text="0", fg="green", bg="white")
        label_error.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)
        self.label_total_error.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.W)
        label_success.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.W)
        self.label_total_success.grid(
            row=0, column=3, padx=5, pady=5, sticky=tk.N + tk.W
        )
        label_time.grid(row=0, column=4, padx=5, pady=5, sticky=tk.N + tk.W)
        self.label_time_re.grid(row=0, column=5, padx=5, pady=5, sticky=tk.N + tk.W)

    def UpdateError(self, text):
        if text:
            self.label_total_error.config(text=str(text))
        else:
            self.label_total_error.config(text="0")

    def UpdateSuccess(self, text):
        if text:
            self.label_total_success.config(text=str(text))
        else:
            self.label_total_success.config(text="0")
