#!/usr/bin/python3
import pathlib
import pygubu
from pathlib import Path
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ascii_file_preview.ui"
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class AsciFilePreview:
    def __init__(self, master=None, filename = None, clipboard = None):
        self.builder = builder = pygubu.Builder()
        self.master = master
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        # --- END OF PYGUBU BUILDER ---

        # References
        self.filename = filename
        self.clipboard = clipboard

        self.name_entry = builder.get_object('name_entry', master)
        if self.filename != None:
            self.name_entry.insert(1, Path(filename).name)

        self.first_lines = builder.get_object('first_lines', master)
        self.first_lines.insert(1, 0)
        self.last_lines = builder.get_object('last_lines', master)
        self.last_lines.insert(1, 0)

        self.first_as_headers = builder.get_object('first_lines', master)
        self.sel_separator = builder.get_object('box_sel_separator', master)
        self.sel_separator.set("Comma")

        self.label_custom = builder.get_object('label_custom', master)
        self.field_custom = builder.get_object('field_custom', master)
        self.field_headers = builder.get_object('field_headers', master)
        self.custom_on(False)
        self.field_headers.delete(1, 'end')
        self.check_headers = builder.get_object('check_headers', master)

        # suwak i pole tekstowe
        self.textframe = builder.get_object('textframe', master)
        scrollbar_y = ttk.Scrollbar(self.textframe, orient="vertical")
        scrollbar_x = ttk.Scrollbar(self.textframe, orient="horizontal")
        self.preview = ctk.CTkTextbox(self.textframe, wrap=tk.NONE, yscrollcommand=scrollbar_y.set,  xscrollcommand=scrollbar_x.set)
        self.preview.pack(expand=True, fill="both")

        # Set as modal
        self.mainwindow.grab_set()
        self.mainwindow.attributes('-topmost', True)
        self.mainwindow.title("Import ASCII file")

        # Keyboard bindings
        self.mainwindow.bind("<Escape>", self.cancel)
        self.first_lines.bind("<Return>", lambda position: self.show_preview(position = 'first'))
        self.first_lines.bind("<KP_Enter>", lambda position: self.show_preview(position='first'))
        self.last_lines.bind("<Return>", lambda position: self.show_preview(position = 'last'))
        self.last_lines.bind("<KP_Enter>", lambda position: self.show_preview(position='last'))
        self.response = {'text':'', 'separator':'Tab', 'name':'', 'headers':''}

        self.read_file()
        self.show_preview()

        self.center_window(self.mainwindow,  700, 500)
    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        ''' This function returns the output from the closed window'''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def ok(self):
        ''' This is activated after clicking OK button'''
        self.response['text'] = self.preview.get(1.0, 'end')
        self.response['name'] = self.name_entry.get()
        separator = self.sel_separator.get()
        if separator == 'Custom':
            self.response['separator'] = self.field_custom.get()
        else:
            self.response['separator'] = separator

        self.mainwindow.destroy()

    ''' END OF MANDATORY METHODS '''

    def sel_separator(self, value):
        if value == 'Custom':
            self.response['separator'] = self.field_custom.get()
        else:
            self.response['separator'] = value

    def custom_on(self, on = False):
        if on:
            self.label_custom.grid()
            self.field_custom.grid()
        else:
            self.label_custom.grid_remove()
            self.field_custom.grid_remove()
    def cancel(self):
        self.response = None
        self.mainwindow.destroy()

    def reload(self):
        self.read_file()
        self.first_lines.delete(0, 'end')
        self.first_lines.insert(0, '0')
        self.last_lines.delete(0, 'end')
        self.last_lines.insert(0, '0')

        self.show_preview()

    def read_file(self):
        if self.clipboard == None:
            try:
                with open(Path(self.filename), 'rb') as file:
                    content = file.read()
                    self.file_content = content.decode('utf-8', errors='ignore')
                    self.show_preview()
            except:
                self.preview.delete(1.0, 'end')
                self.preview.insert(1.0, "ERROR. The file could not be loaded.")
        else:
            self.file_content = self.clipboard

    def show_preview(self, event=None, position = 'first'):
        n_first_lines = int(self.first_lines.get())
        n_last_lines = int(self.last_lines.get())
        text = self.file_content.split('\n')
        if n_last_lines > 0:
            text = text[:-n_last_lines]

        if n_first_lines > 0:
            text = text[n_first_lines:]
        text_without_lines = '\n'.join(text)
        self.response['text'] = text_without_lines
        self.response['headers'] = self.field_headers.get()
        self.preview.delete('1.0', 'end')
        self.preview.insert('1.0', self.response.get('text', ""))

        if position == 'last':
            self.preview.see('end')

    def first_as_headers(self):
        if self.check_headers.get() == 1:
            self.field_headers.delete(0, 'end')
            headers = self.file_content.split('\n')[0]
            self.field_headers.insert(1, headers)
            n_first_lines = int(self.first_lines.get())
            if n_first_lines == 0:
                self.first_lines.delete(0, 'end')
                self.first_lines.insert(0, '1')
                self.show_preview()
        else:
            self.field_headers.delete(0, 'end')
            self.first_lines.delete(0, 'end')
            self.first_lines.insert(0, '0')
            self.read_file()



if __name__ == "__main__":
    app = AsciFilePreview()
    app.run()
