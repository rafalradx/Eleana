#!/usr/bin/python3
import pathlib
import pygubu
import pyperclip
import tkinter as tk
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "notepad.ui"


class Notepad:
    def __init__(self, master=None, title = "Notepad", text = None):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        # Set as modal
        self.mainwindow.grab_set()
        self.mainwindow.attributes('-topmost', True)
        self.mainwindow.title(title)

        # Reference to widgets
        self.textbox = builder.get_object("textbox", master)
        self.textbox.focus_set()
        self.btn_clipboard = builder.get_object("btn_clipboard", master)

        # Keyboard bindings
        self.mainwindow.bind("<Escape>", self.cancel)
        self.mainwindow.bind("<Control-c>", self.copy_to_clipboard)
        self.textbox.bind("<Control-c>", self.copy_to_clipboard)
        self.mainwindow.bind("<Control-v>", self.paste_from_clipboard)
        self.response = None

        if text != None:
            self.textbox.insert(1.0, text)
    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''

    def get(self):
        ''' This function returns the output from the closed window'''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        ''' This is activated after clicking OK button'''
        self.response = self.textbox.get("1.0", tk.END)
        self.mainwindow.destroy()
    ''' END OF MANDATORY METHODS '''

    def copy_to_clipboard(self, event = None):
        pyperclip.copy(self.textbox.get(1.0, tk.END))

    def paste_from_clipboard(self):
        text = pyperclip.paste()
        self.textbox.insert(text)

    def clear(self):
        self.textbox.delete(1.0, tk.END)
        self.response = ""
    def cancel(self, event = None):
        self.response = None
        self.mainwindow.destroy()

if __name__ == "__main__":
    app = Notepad()
    app.run()
