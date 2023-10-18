from customtkinter import (CTkButton, CTkFrame, CTkTextbox, CTkToplevel)

class Groupeditor:
    def __init__(self, eleana_instance, master=None):
        # Store the main window
        self.master = master
        self.eleana = eleana_instance
        # Create a Toplevel window for the modal dialog
        self.modal_window = CTkToplevel(master)
        self.modal_window.grab_set()  # Ustaw okno modalne
        self.modal_window.attributes('-topmost', True)  # Ustaw na zawsze na wierzchu

        # Build UI for the modal window
        ctkframe2 = CTkFrame(self.modal_window)
        self.ctktextbox1 = CTkTextbox(ctkframe2)  # Zmieniamy na self.ctktextbox1
        _text_ = 'Jakiś tekst'
        self.ctktextbox1.insert("0.0", _text_)
        self.ctktextbox1.grid(column=0, row=0)
        ctkbutton2 = CTkButton(ctkframe2)
        ctkbutton2.configure(text='OK')
        ctkbutton2.grid(column=0, row=1)
        ctkframe2.grid(column=0, row=0)

        # Store the response variable
        self.response = None

        # Set up the OK button command
        ctkbutton2.configure(command=self.close_this)

    def run(self):
        self.modal_window.mainloop()

    def close_this(self):
        # Set the response to the text in the textbox and close the modal window
        self.response = self.ctktextbox1.get("1.0", "end-1c")  # Używamy self.ctktextbox1
        self.modal_window.destroy()

    def get(self):
        if self.modal_window.winfo_exists():
            self.master.wait_window(self.modal_window)
        print(self.eleana.selections)
        return self.response

if __name__ == "__main__":
    root = CTkToplevel()
    app = Groupeditor(root)
    app.run()
    response = app.get()
    print(response)
