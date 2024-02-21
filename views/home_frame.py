import tkinter as tk
from tkinter.ttk import Treeview, Style
from config import SUCCESS, ERROR, RUN


class HomeFrame(tk.Frame):
    def __init__(self, window, cnf={}, **kwargs):
        tk.Frame.__init__(self, window, **kwargs, bg="white")
        self.tree = self.TreeViewAccount()
        # for i in range(1, 100):
        #     self.InsertAccount(f"gmail{i}", f"password{i}", f"status{i}")

    def TreeViewAccount(self):
        tree = Treeview(
            self,
            columns=("Gmail", "Password", "Status"),
            show="headings",
            height=19,
        )
        style = Style(tree)
        style.configure("Treeview", rowheight=28)
        tree.column("Gmail", width=130, anchor=tk.CENTER)
        tree.column("Password", width=130, anchor=tk.CENTER)
        tree.column("Status", width=440, anchor=tk.CENTER)
        tree.heading("Gmail", text="Gmail")
        tree.heading("Password", text="Mật khẩu")
        tree.heading("Status", text="Trạng thái")
        tree.tag_configure(SUCCESS, foreground="black", background="white")
        tree.tag_configure(ERROR, foreground="white", background="red")
        tree.tag_configure(RUN, foreground="white", background="green")
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        return tree

    def InsertAccount(self, gmail, password, status):
        self.tree.insert(
            "",
            "end",
            values=(
                f"{gmail}",
                f"{password}",
                f"{status}",
            ),
        )
        self.tree.see(self.tree.get_children()[-1])

    def UpdateAccount(self, gmail, password, status, tag):
        for item in self.tree.get_children():
            current_gmail = self.tree.item(item, "values")[0]
            if current_gmail == gmail:
                self.tree.item(
                    item,
                    values=(
                        self.tree.item(item, "values")[0],
                        f"{password}",
                        f"{status}",
                    ),
                    tags=(tag,),
                )
                break
