#!/usr/bin/python3
import tkinter as tk
from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkSlider)


class CTkHorizontalSlider(CTkFrame):
    def __init__(self, title='', direction = 'ver', range=[0,1], master=None, app_instance=None, **kw):
        self.app = app_instance
        self.direction = direction
        super(CTkHorizontalSlider, self).__init__(master, **kw)
        self.sliderFrame = CTkFrame(self)
        self.sliderFrame.grid_columnconfigure(0, weight=2)
        self.sliderFrame.grid_columnconfigure(1, weight=1)

        ctklabel1 = CTkLabel(self.sliderFrame)
        ctklabel1.configure(text=title)
        ctklabel1.grid(column=0, row=0, sticky="w", columnspan=3)
        self.slider = CTkSlider(self.sliderFrame)
        self.slider.configure(from_=range[0], number_of_steps=40, to=range[1])
        self.slider.grid(column=0, columnspan=1, row=1, sticky="ew")
        self.slider.configure(command=self.set_increment)
        self.reset()
        self.factor = CTkEntry(self.sliderFrame)
        #self.factor.configure(state="active", width=50)
        self.factor.grid(column=1, padx=2, row=1, sticky="ew")
        self.btn_reset = CTkButton(self.sliderFrame)
        self.btn_reset.configure(text='Reset', width=20, command=self.reset)
        self.btn_reset.grid(column=2, padx=2, row=1, sticky="ew")
        self.btn_reset.configure(command=self.reset)
        self.sliderFrame.grid(column=0, row=0, sticky="nsew")
        self.sliderFrame.columnconfigure(0, weight=1)
        self.configure(height=200, width=200)
        self.columnconfigure(0, weight=1)
        self.factor.insert(0, "1" )

        self.increment = 0
        self.factor.bind("<Return>", self.set_increment)


    def reset(self):
        self.slider.set(0)
        self.increment = 0

    def set_increment(self, event = None):
        factor = float(self.factor.get())
        slider = self.slider.get()
        self.increment = factor * slider
        self.app.separate_plots_by(self.direction, self.increment)

if __name__ == "__main__":
    root = tk.Tk()
    widget = CTkHorizontalSlider(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
