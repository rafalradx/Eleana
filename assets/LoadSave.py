from pathlib import Path
import pathlib
import json
import subprocess
from customtkinter import filedialog
#from assets.general_eleana_methods import Eleana

import pickle
from tkinter.filedialog import asksaveasfile, askopenfilename
import random
import shutil
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from assets.DataClasses import createFromElexsys


class Load:
    def __init__(self, eleana_instance):
        self.eleana = eleana_instance
    # FILE
    def load_project(self, recent=None):
        ''' This method loads projects created by Eleana'''

        init_dir = Path(self.eleana.paths['last_project_dir'])
        try:
            init_file = Path(self.eleana.paths['last_projects'][0])
            init_file = init_file.name
        except IndexError:
            init_dir = Path(self.eleana.paths['home_dir'])
            init_file = ''

        if recent == None:
            filename =  askopenfilename(initialdir=init_dir,
                                     initialfile=init_file,
                                     defaultextension=".ele",
                                     filetypes=[("Eleana project", "*.ele"),
                                                ("All Files", "*.*")])
        else:
            filename = Path(recent)

        '''
        1. Extract project into temporary directory /tmp/eleana_extracted_project 
        '''
        tmp_folder = 'eleana_extracted_project'
        extract_dir = Path(self.eleana.paths['tmp_dir'], tmp_folder)
        archive_format = 'zip'
        try:
            shutil.unpack_archive(filename, extract_dir, archive_format)
        except:
            return {"Error": True, 'desc': f"Cannot open the file"}


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

            if float(project_version) > float(self.eleana.version):
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
            eleana_assignmentToGroups = {}
            for each in loaded_object:
                group, value = list(each.items())[0]
                eleana_assignmentToGroups[group] = value
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

    # Import EPR
    def loadElexsys(self) -> object:
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('Elexsys', '*.DSC'),
            ('All files', '*.*')
            )
        filenames = filedialog.askopenfilenames(initialdir=path, filetypes=filetypes)
        if len(filenames) == 0:
            return
        for file in filenames:
            spectrum = createFromElexsys(file)
            self.eleana.dataset.append(spectrum)
        last_import_dir = Path(filenames[-1]).parent
        self.eleana.paths['last_import_dir'] = last_import_dir
        return

class Save:
    def __init__(self, eleana_instance):
        self.eleana = eleana_instance
    def save_project(self):
        try:
            init_dir = Path(self.eleana.paths['last_project_dir'])
            init_file = ''
        except IndexError:
            init_dir = Path(self.eleana.paths['home_dir'])

        try:
            filename = asksaveasfile(initialdir=init_dir,
                                 initialfile=init_file,
                                 defaultextension=".ele",
                                 filetypes=[("All Files", "*.*"),
                                            ("Eleana project", "*.ele")])
        except:
            return {'error': True, 'desc': f'Could not save the project file. Try to save in different location.'}

        file_path = Path(filename.name)
        file_path.unlink()

        # Create random name of working directory
        working_folder = filename.name + '__' + str(random.randint(1000000,9999999))
        new_directory = Path(working_folder)
        try:
            new_directory.mkdir(parents=True, exist_ok=True)
        except:
            return {"error": True, 'desc': f"Could not create working dir while saving {filename.name}"}

        '''
        Create list of names for eleana.dataset
        '''
        dataset_names = {}
        i = 0
        for each in self.eleana.dataset:
            name = each.name_nr
            name = name.replace('. ', '_=_')
            dataset_names[str(i)] = name
            i += 1

        results_names = {}
        i = 0
        for each in self.eleana.results_dataset:
            name = each.name_nr
            name = name.replace('. ', '_=_')
            results_names[str(i)] = name
            i += 1

        project_details = {'project version':'1.0'}

        ordered_groups = []
        for group, spectra in self.eleana.assignmentToGroups.items():
            ordered_groups.append({group: spectra})

        elements_to_save = {
                            'eleana_assignmentToGroups':ordered_groups,
                            'eleana_groupsHierarchy':self.eleana.groupsHierarchy,
                            'eleana_notes':self.eleana.notes,
                            'eleana_paths':self.eleana.paths,
                            'eleana_selections':self.eleana.selections,
                            'eleana_dataset_list':dataset_names,
                            'eleana_results_list':results_names,
                            'eleana_results_dataset':self.eleana.results_dataset,
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
                    pickle.dump(self.eleana.dataset[i], file)
                i += 1

            ''' 
            Save result dataset
            '''
            i = 0
            for each in self.eleana.results_dataset:
                name = 'r' + str(i)
                data_file = Path(working_folder, name)
                with open(data_file, 'wb') as file:
                    pickle.dump(self.eleana.results_dataset[i], file)
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
            return {"error": False, 'desc':'', 'return':filename}
        except:
            return {"error": True, 'desc': f"Error while saving {filename.name}"}
