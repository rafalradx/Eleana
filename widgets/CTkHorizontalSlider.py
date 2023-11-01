#!/usr/bin/python3
import tkinter as tk
from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkSlider)


class CTkHorizontalSlider(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super(CTkHorizontalSlider, self).__init__(master, **kw)
        self.sliderFrame = CTkFrame(self)
        ctklabel1 = CTkLabel(self.sliderFrame)
        ctklabel1.configure(text='Change separation vertically')
        ctklabel1.grid(column=0, row=0, sticky="w")
        self.slider = CTkSlider(self.sliderFrame)
        self.slider.configure(from_=-1, number_of_steps=100, to=1)
        self.slider.grid(column=0, columnspan=1, row=1, sticky="nsew")
        self.slider.configure(command=self.slider_change)
        self.factor = CTkEntry(self.sliderFrame)
        #self.factor.configure(state="active", width=50)
        self.factor.grid(column=1, padx=2, row=1, sticky="nsew")
        self.btn_reset = CTkButton(self.sliderFrame)
        self.btn_reset.configure(text='Reset', width=50)
        self.btn_reset.grid(column=2, padx=2, row=1, sticky="nsew")
        self.btn_reset.configure(command=self.reset)
        self.sliderFrame.grid(column=0, row=0, sticky="nsew")
        self.sliderFrame.columnconfigure(0, weight=1)
        self.configure(height=200, width=200)
        self.columnconfigure(0, weight=1)

    def slider_change(self, value):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = CTkHorizontalSlider(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
