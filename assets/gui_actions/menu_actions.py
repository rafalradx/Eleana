from pathlib import Path
import json
import subprocess
from customtkinter import filedialog
from assets.general_eleana_methods import Eleana
from assets.modules.bruker_elexsys import Elexsys
import pickle
from tkinter.filedialog import asksaveasfile, askopenfilename
import random
import shutil
# Create instances
elexsys = Elexsys()
eleana = Eleana()

class MenuAction():
    # FILE
    def load_project(self, eleana: object):
        filename =  askopenfilename(initialdir=eleana.paths['last_project_dir'],
                                 initialfile=eleana.paths['last_project'],
                                 defaultextension=".elp",
                                 filetypes=[("Eleana project", "*.elp"),
                                            ("All Files", "*.*")])

        extract_dir = eleana.paths['tmp_dir']
        tmp_folder = 'eleana_extracted_project'
        extract_dir = Path(eleana.paths['tmp_dir'], tmp_folder)
        archive_format = 'zip'
        try:
            shutil.unpack_archive(filename, extract_dir, archive_format)
        except:
            return {"Error": True, 'desc': f"Cannot open {filename.name}"}

        eleana_dataset = Path(extract_dir, 'eleana_dataset')
        eleana_results_dataset = Path(extract_dir, 'eleana_results_dataset')
        eleana_assignmentsToGroups = Path(extract_dir, 'eleana_assignmentsToGroups')
        eleana_groupsHierarchy = Path(extract_dir, 'eleana_groupsHierarchy')
        eleana_notes = Path(extract_dir, 'eleana_notes')
        eleana_paths = Path(extract_dir, 'eleana_paths')
        eleana_selections = Path(extract_dir, 'eleana_selections')

        # Load selections
        file_to_read = open(eleana_selections, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.selections = loaded_object
        file_to_read.close()

        # Load paths
        file_to_read = open(eleana_paths, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.paths = loaded_object
        file_to_read.close()

        # Load notes
        file_to_read = open(eleana_notes, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.notes = loaded_object
        file_to_read.close()

        # Load groupsHierarchy
        file_to_read = open(eleana_groupsHierarchy, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.groupsHierarchy = loaded_object
        file_to_read.close()

        # Load assignmentsToGroups
        file_to_read = open(eleana_assignmentsToGroups, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.assignmentsToGroups = loaded_object
        file_to_read.close()

        # Load results_dataset
        file_to_read = open(eleana_results_dataset, "rb")
        loaded_object = pickle.load(file_to_read)
        eleana.results_dataset = loaded_object
        file_to_read.close()



    def save_as(self, eleana: object):
        filename = asksaveasfile(initialdir=eleana.paths['last_project_dir'],
                                 initialfile=eleana.paths['last_project'],
                                 defaultextension=".elp",
                                 filetypes=[("All Files", "*.*"),
                                            ("Eleana project", "*.elp")])
        file_path = Path(filename.name)
        file_path.unlink()

        working_folder = filename.name + '__' + str(random.randint(1000000,9999999))
        new_directory = Path(working_folder)
        new_directory.mkdir(parents=True, exist_ok=True)

        elements_to_save = {'eleana_dataset':eleana.dataset,
                            'eleana_results_dataset':eleana.results_dataset,
                            'eleana_assignmentsToGroups':eleana.assignmentToGroups,
                            'eleana_groupsHierarchy':eleana.groupsHierarchy,
                            'eleana_notes':eleana.notes,
                            'eleana_paths':eleana.paths,
                            'eleana_selections':eleana.selections
                            }
        # Save the eleana atributes to separate files
        # Names for files are taken form keys of element_to_save
        try:
            for each in elements_to_save.keys():
                file_path = Path(new_directory, each)
                with open(file_path, 'wb') as file:
                    pickle.dump(elements_to_save[each], file)

            # Create zip file form the directory
            name_without_extension = filename.name[:-4]
            shutil.make_archive(name_without_extension, 'zip', new_directory)
            zip_file = Path(name_without_extension + '.zip')
            new_name = zip_file.with_suffix(".elp")

            # Rename zip to elp
            zip_file.rename(new_name)

            # Remove files in workin_dir
            for file in new_directory.glob('*'):
                file.unlink()

            # Remove workin dir
            new_directory.rmdir()
        except:
            return {"Error": True, 'desc': f"Error while saving {filename.name}"}






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