import tkinter as tk
import tkinter.ttk as ttk
import threading
import subprocess
import sys

interpreter = sys.executable
class SplashScreenApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("702x370")
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        label1 = ttk.Label(frame1)
        self.img_splash700x352 = tk.PhotoImage(file="pixmaps/splash700x352.png")
        label1.configure(
            background="#000000",
            image=self.img_splash700x352,
            text='label1')
        label1.grid(column=0, row=0)
        self.progress = ttk.Progressbar(frame1)
        self.progress_var = tk.IntVar()
        self.progress.configure(
            orient="horizontal",
            variable=self.progress_var)
        self.progress.grid(column=0, row=1, sticky="sew")
        frame1.grid(column=0, row=0)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

def load_main():
    try:
        subprocess.run([interpreter, "main.py"])
    except Exception as e:
        print("Error starting Eleana")

def update_progress():
    if app.progress_var.get() >= 100:
        load_thread = threading.Thread(target=load_main)
        load_thread.start()
    else:
        app.progress_var.set(app.progress_var.get() + 1)
        app.mainwindow.after(5, update_progress)

if __name__ == "__main__":
    app = SplashScreenApp()
    app.mainwindow.overrideredirect("true")
    width = app.mainwindow.winfo_screenwidth()
    height = app.mainwindow.winfo_screenheight()

    left_pos = int((width/2) - (702 / 2))
    top_pos = int((height/2) - (370/2))

    app.mainwindow.geometry('702x370+' + str(left_pos) + '+' + str(top_pos))

    update_progress()

    # Set splash screen time in seconds
    splash_duration = 3.5  # seconds

    # Close after completion
    app.mainwindow.after(int(splash_duration * 1000), app.mainwindow.destroy)

    app.run()
