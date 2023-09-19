from pathlib import Path
import json
import subprocess
from customtkinter import filedialog
from assets.general_eleana_methods import Eleana
from assets.modules.bruker_elexsys import Elexsys

# Create instances
elexsys = Elexsys()
eleana = Eleana()

class MenuAction():
    # FILE
    # Import EPR
    def loadElexsys(self) -> object:
        filetypes = (
            ('Elexsys', '*.DSC'),
            ('All files', '*.*')
            )
        filenames = filedialog.askopenfilenames(initialdir=eleana.paths['last_import_dir'], filetypes=filetypes)
        if len(filenames) == 0:
            return

        for file in filenames:
            spectrum = elexsys.read(file)
            eleana.dataset.append(spectrum)
        return eleana.dataset

    # EDIT
    #       Notes
    def notes(self):
        content_to_sent = eleana.notes
        content_to_sent.update({'window_title': 'Edit notes'})  # Add text for window title

        filename = "eleana_edit_notes.rte"
        formatted_str = json.dumps(content_to_sent, indent=4)

        # Create /tmp/eleana_edit_notes.rte
        Eleana.create_tmp_file(self, filename, formatted_str)
        subprocess_path = Path(eleana.paths['assets'], 'subprogs', 'editor.py')
        # Run editor in subprocess_path (./assets/edit.py) and wait for end
        notes = subprocess.run([eleana.interpreter, subprocess_path], capture_output=True, text=True)

        return filename