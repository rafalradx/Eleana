#!/usr/bin/python3
import tkinter as tk
from customtkinter import (CTkButton, CTkLabel)


class QuitDialog:
    def __init__(self, master=None):
        self.result = None
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, padx=10, pady=10, width=200)
        toplevel1.title("Quit")
        ctklabel1 = CTkLabel(toplevel1)
        ctklabel1.configure(
            justify="center",
            text='Do you really want to quit?')
        ctklabel1.grid(column=0, columnspan=2, row=0)
        self.btn_quit = CTkButton(toplevel1)
        self.btn_quit.configure(text='Yes, quit')
        self.btn_quit.grid(column=0, padx=10, pady=10, row=1)
        self.btn_quit.configure(command=self.quit_appication)
        self.btn_cancel_quit = CTkButton(toplevel1)
        self.btn_cancel_quit.configure(text='Cancel')
        self.btn_cancel_quit.grid(column=1, row=1)
        self.btn_cancel_quit.configure(command=self.cancel_quit)

        # Main widget
        self.mainwindow = toplevel1

        self.decission = ""
    def run(self):
        self.mainwindow.mainloop()

    def quit_appication(self):
        app.mainwindow.destroy()

    def cancel_quit(self):
        print("cancel")
        app.mainwindow.destroy()

if __name__ == "__main__":
    app = QuitDialog()
    app.run()



