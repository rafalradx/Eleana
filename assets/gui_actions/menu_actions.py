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
import tkinter as tk
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox

# Create instances
elexsys = Elexsys()
eleana = Eleana()

class MenuAction():
    # FILE

    def load_project(self, eleana: object):
        ''' This method loads projects created by Eleana'''

        filename =  askopenfilename(initialdir=eleana.paths['last_project_dir'],
                                     initialfile=eleana.paths['last_project'],
                                     defaultextension=".ele",
                                     filetypes=[("Eleana project", "*.ele"),
                                                ("All Files", "*.*")])

        '''
        1. Extract project into temporary directory /tmp/eleana_extracted_project 
        '''
        tmp_folder = 'eleana_extracted_project'
        extract_dir = Path(eleana.paths['tmp_dir'], tmp_folder)
        archive_format = 'zip'
        try:
            shutil.unpack_archive(filename, extract_dir, archive_format)
        except:
            return {"Error": True, 'desc': f"Cannot open {filename.name}"}


        ''' 
        2. Define filenames that will be loaded from unzipped project
        '''
        eleana_dataset_list = Path(extract_dir, 'eleana_dataset_list')
        eleana_assignmentToGroups = Path(extract_dir, 'eleana_assignmentToGroups')
        eleana_groupsHierarchy = Path(extract_dir, 'eleana_groupsHierarchy')
        eleana_notes = Path(extract_dir, 'eleana_notes')
        eleana_paths = Path(extract_dir, 'eleana_paths')
        eleana_selections = Path(extract_dir, 'eleana_selections')
        eleana_results_dataset: Path = Path(extract_dir, 'eleana_results_dataset')
        eleana_project_details = Path(extract_dir, 'eleana_project_details')
        eleana_dataset = Path(extract_dir, 'eleana_dataset')

        try:
            '''
            3. Load eleana_project_details to check if its compatible with the current Eleana version
            '''

            file_to_read = open(eleana_project_details, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_project_details = loaded_object
            file_to_read.close()

            project_version = float(loaded_object['project version'])

            if project_version > eleana.version:
                info = CTkMessagebox(title="Project load", message='This project was created in newer Eleana version. Some errors in loaded content are possible')

            '''
            4. Load eleana_XXXXX files and store the content in temporary variables  
            '''

            # LOAD: eleana_selections

            file_to_read = open(eleana_selections, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_selections = loaded_object
            file_to_read.close()

            # LOAD eleana_paths

            file_to_read = open(eleana_paths, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_paths = loaded_object
            file_to_read.close()

            # LOAD notes

            file_to_read = open(eleana_notes, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_notes = loaded_object
            file_to_read.close()

            # LOAD groupsHierarchy

            file_to_read = open(eleana_groupsHierarchy, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_groupsHierarchy = loaded_object
            file_to_read.close()

            # LOAD assignmentsToGroups

            file_to_read = open(eleana_assignmentToGroups, "rb")
            loaded_object = pickle.load(file_to_read)
            assignmentToGroups = loaded_object
            file_to_read.close()

            '''
            5. Load list of the objects to store in eleana.dataset
            '''
            # LOAD results_dataset

            file_to_read = open(eleana_results_dataset, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_results_dataset = loaded_object
            file_to_read.close()

            # LOAD dataset

            file_to_read = open(eleana_dataset_list, "rb")
            loaded_object = pickle.load(file_to_read)
            eleana_dataset_list = loaded_object
            file_to_read.close()


            eleana_dataset = []
            for filenumber in eleana_dataset_list.keys():
                filename = Path(extract_dir, filenumber)
                file_to_read = open(filename, "rb")
                loaded_object = pickle.load(file_to_read)
                eleana_dataset.append(loaded_object)
                file_to_read.close()

        except:
            return {"Error": True, 'desc': f"An error occured while loading the file"}

        '''
        6. Remove all files from extract_directory and then remove extract directory
        '''
        try:
            for file in extract_dir.iterdir():
                if file.is_file():
                    file.unlink()
        except:
            pass

        try:
            extract_dir.rmdir()
        except:
            pass

        return {'dataset':eleana_dataset,
                'result_dataset':eleana_results_dataset,
                'assignmentToGroups': eleana_assignmentToGroups,
                'groupsHierarchy':eleana_groupsHierarchy,
                'notes':eleana_notes,
                'paths':eleana_paths,
                'selections':eleana_selections,
                'results_dataset':eleana_results_dataset
                }



    def save_as(self, eleana: object):
        filename = asksaveasfile(initialdir=eleana.paths['last_project_dir'],
                                 initialfile=eleana.paths['last_project'],
                                 defaultextension=".ele",
                                 filetypes=[("All Files", "*.*"),
                                            ("Eleana project", "*.ele")])
        file_path = Path(filename.name)
        file_path.unlink()

        # Create random name of working directory
        working_folder = filename.name + '__' + str(random.randint(1000000,9999999))
        new_directory = Path(working_folder)
        try:
            new_directory.mkdir(parents=True, exist_ok=True)
        except:
            return {"Error": True, 'desc': f"Could not create working dir while saving {filename.name}"}

        '''
        Create list of names for eleana.dataset
        '''
        dataset_names = {}
        i = 0
        for each in eleana.dataset:
            name = each.name_nr
            name = name.replace('. ', '_=_')
            dataset_names[str(i)] = name
            i += 1

        results_names = {}
        i = 0
        for each in eleana.results_dataset:
            name = each.name_nr
            name = name.replace('. ', '_=_')
            results_names[str(i)] = name
            i += 1

        project_details = {'project version':'1.0'}

        elements_to_save = {
                            'eleana_assignmentToGroups':eleana.assignmentToGroups,
                            'eleana_groupsHierarchy':eleana.groupsHierarchy,
                            'eleana_notes':eleana.notes,
                            'eleana_paths':eleana.paths,
                            'eleana_selections':eleana.selections,
                            'eleana_dataset_list':dataset_names,
                            'eleana_results_list':results_names,
                            'eleana_results_dataset':eleana.results_dataset,
                            'eleana_project_details':project_details
                            }

        try:
            # Save the eleana attributes to separate files
            # Names for files are taken form keys of element_to_save
            for each in elements_to_save.keys():
                file_path = Path(new_directory, each)
                with open(file_path, 'wb') as file:
                    pickle.dump(elements_to_save[each], file)

            '''
            Each object in eleana.dataset will be saved 
            using pickle as a separate file, for which name is
            the numeber in the eleana.dataset list.
            Additionally the list of dataset names is saved in dataset_list
            '''
            i = 0
            for name in dataset_names.keys():
                data_file = Path(working_folder, str(i))
                with open(data_file, 'wb') as file:
                    pickle.dump(eleana.dataset[i], file)
                i += 1

            ''' 
            Save result dataset
            '''
            i = 0
            for each in eleana.results_dataset:
                name = 'r' + str(i)
                data_file = Path(working_folder, name)
                with open(data_file, 'wb') as file:
                    pickle.dump(eleana.results_dataset[i], file)
                i += 1

            # Create zip file form the directory
            name_without_extension = filename.name[:-4]
            shutil.make_archive(name_without_extension, 'zip', new_directory)
            zip_file = Path(name_without_extension + '.zip')
            new_name = zip_file.with_suffix(".ele")

            # Rename zip to ele
            zip_file.rename(new_name)

            # Remove files in working_dir
            for file in new_directory.glob('*'):
                file.unlink()

            # Remove working dir
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