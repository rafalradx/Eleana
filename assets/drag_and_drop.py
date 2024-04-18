import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

def on_drop(event):
    print(event.data)
    file_path = event.data
    entry_var.set(file_path)

# Tworzenie głównego okna
root = TkinterDnD.Tk()

# Ustawienia okna
root.title("Przeciągnij plik")
root.geometry("300x150")

# Pole tekstowe do wyświetlania ścieżki pliku
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, width=30)
entry.pack(pady=20)

# Funkcja obsługująca przeciąganie
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', on_drop)

# Uruchamianie głównej pętli programu
root.mainloop()