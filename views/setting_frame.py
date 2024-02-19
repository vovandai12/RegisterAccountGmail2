from tkinter import Frame
from tkinter import (
    Tk,
    N,
    W,
    Y,
    S,
    E,
    END,
    VERTICAL,
    LEFT,
    RIGHT,
    CENTER,
    BOTH,
    INSERT,
    NSEW,
    Scrollbar,
    Frame,
    Label,
    Frame,
    Text,
    Button,
    Entry,
    LabelFrame,
    StringVar,
    OptionMenu,
    Radiobutton,
    Spinbox,
    Checkbutton,
)


class SettingFrame(Frame):
    def __init__(self, window, cnf={}, **kwargs):
        Frame.__init__(self, window, **kwargs, bg="red")
