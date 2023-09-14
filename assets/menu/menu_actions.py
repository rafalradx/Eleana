from customtkinter import filedialog
from assets.general_eleana_methods import Eleana
from assets.modules.bruker_elexsys import Elexsys
class MenuAction():
    def loadElexsys(self) -> object:
        filetypes = (
            ('Elexsys', '*.DSC'),
            ('All files', '*.*')
            )

        filenames = filedialog.askopenfilenames(initialdir=Eleana.paths['last_import_dir'], filetypes=filetypes)
        if len(filenames) == 0:
            return

        elexsys = Elexsys()
        for file in filenames:
            spectrum = elexsys.read(file)
            Eleana.dataset.append(spectrum)

        return Eleana.dataset

    def quit(self):
        decission = subprocess.run(["python3", "libs/quit_dialog.py"], capture_output=True, text=True)
        print(decission.stdout[:4])
        if decission.stdout[:4] == "quit":
            app.mainwindow.destroy()

