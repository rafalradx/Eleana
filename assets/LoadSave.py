from pathlib import Path
import string
import copy
import pickle
import json
from tkinter.filedialog import asksaveasfile, askopenfilename
import random
import shutil
from tkinter import filedialog
import pandas
import numpy as np
from modules.CTkMessagebox.ctkmessagebox import CTkMessagebox
from assets.DataClasses import createFromElexsys, createFromEMX, createFromShimadzuSPC, createFromMagnettech, createFromAdaniDat
from assets.Error import Error
from subprogs.ascii_file_preview.ascii_file_preview import AsciFilePreview
from subprogs.table.table import CreateFromTable

class Load:
    def __init__(self, eleana):
        self.eleana = eleana
        #self.menu = menu_instance
        #self.app = self.menu.app
        #self.eleana = eleana
        pass

    # @staticmethod
    # def load_preferences(eleana):
    #     ''' Load saved graph settings from home/.EleanaPy/preferences.pic'''
    #     try:
    #         filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'preferences.pic')
    #         # Read paths.pic
    #         file_to_read = open(filename, "rb")
    #         settings = pickle.load(file_to_read)
    #         file_to_read.close()
    #         return settings
    #     except Exception as e:
    #         print(e)
    #         return None

    # @classmethod
    # def load_paths_settings(cls, eleana):
    #     ''' Load saved settings from home/.EleanaPy/paths.pic'''
    #     try:
    #         filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')
    #         # Read paths.pic
    #         file_to_read = open(filename, "rb")
    #         paths = pickle.load(file_to_read)
    #         eleana.paths = paths
    #         file_to_read.close()
    #         # Create last project list in the main menu
    #         last_projects = eleana.paths['last_projects']
    #         last_projects = [element for i, element in enumerate(last_projects) if i <= 10]
    #         # Write the list to eleana.paths
    #         eleana.paths['last_projects'] = last_projects
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return None

    def load_project(self, recent=None):
        ''' This method loads projects created by Eleana'''

        def _update_last_projects(filename):
            last_projects = self.eleana.paths['last_projects']
            filename = str(filename)
            if filename in last_projects:
                index = last_projects.index(filename)
                last_projects.pop(index)
            last_projects.insert(0, filename)
            self.eleana.save_paths()
            self.eleana.paths['last_projects'] = last_projects
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
        if not filename:
            return None

        # Extract project into temporary directory /tmp/eleana_extracted_project
        tmp_folder = 'eleana_extracted_project' + str(random.randint(0,1000))
        extract_dir = Path(self.eleana.paths['tmp_dir'], tmp_folder)
        archive_format = 'zip'
        try:
            if not Path.exists(Path(filename)):
                raise FileExistsError('File not found.')
            shutil.unpack_archive(filename, extract_dir, archive_format)
            # Check project version
            info_file = Path(extract_dir, 'info.txt')
            info = info_file.read_text()
            info = json.loads(info)
            project_version = float(info['project version'])
            # Throw error if project version is higher than Eleana version
            if project_version > self.eleana.version:
                Error.show(info="Cannot load the project file.", details="The project was created using a newer version of Eleana.")
                return None
            # Load Project_1
            path_to_project = Path(extract_dir, 'project_1')
            file_to_read = open(path_to_project, "rb")
            loaded_object = pickle.load(file_to_read)
            file_to_read.close()
            try:
                shutil.rmtree(path_to_project.parent)
            except:
                pass

            # Make copy in case of errors
            copy_of_eleana_dataset = copy.deepcopy(self.eleana.dataset)
            copy_of_eleana_results_dataset = copy.deepcopy(self.eleana.results_dataset)
            copy_of_eleana_groupsHierarchy = copy.deepcopy(self.eleana.groupsHierarchy)
            copy_of_eleana_notes = copy.deepcopy(self.eleana.notes)
            copy_of_eleana_selections = copy.deepcopy(self.eleana.selections)
            copy_of_eleana_static_plots = copy.deepcopy(self.eleana.storage.static_plots)

            # Check if dataset is empty
            if len(self.eleana.dataset) > 0:
                # DATASET NOT EMPTY
                question = CTkMessagebox(title="Dataset is not empty",
                                         message="There is data in the dataset. Choose what you want to",
                                         icon="question", option_3="Append to the dataset",
                                         option_2="Replace the dataset",
                                         option_1="Cancel")
                response = question.get()
                if response == None or response == 'Cancel':
                    return None
                elif response == 'Replace the dataset':
                    self.eleana.dataset = copy.deepcopy(loaded_object.dataset)
                    self.eleana.results_dataset = copy.deepcopy(loaded_object.results_dataset)
                    self.eleana.groupsHierarchy = copy.deepcopy(loaded_object.groupsHierarchy)
                    self.eleana.notes = copy.deepcopy(loaded_object.notes)
                    self.eleana.selections = copy.deepcopy(loaded_object.selections)
                    self.eleana.static_plots = copy.deepcopy(loaded_object.static_plots)
                    _update_last_projects(filename)
                    self.menu.create_showplots_menu()
                else:
                    self.eleana.dataset.extend(copy.deepcopy(loaded_object.dataset))
                    self.eleana.results_dataset.extend(copy.deepcopy(loaded_object.results_dataset))
                    self.eleana.static_plots.extend(copy.deepcopy(loaded_object.static_plots))
                    self.menu.create_showplots_menu()
                    _update_last_projects(filename)
            # If success return True
            else:
                # DATASET IS EMPTY
                self.eleana.dataset = copy.deepcopy(loaded_object.dataset)
                self.eleana.results_dataset = copy.deepcopy(loaded_object.results_dataset)
                self.eleana.groupsHierarchy = copy.deepcopy(loaded_object.groupsHierarchy)
                self.eleana.notes = copy.deepcopy(loaded_object.notes)
                self.eleana.selections = copy.deepcopy(loaded_object.selections)
                self.eleana.static_plots = copy.deepcopy(loaded_object.static_plots)
                _update_last_projects(filename)
                #self.create_showplots_menu()
            return True
        except Exception as e:
            Error.show(info="Cannot load the project file", details=e)
            # Restore Eleana project values from the state before loading
            self.eleana.dataset = copy_of_eleana_dataset
            self.eleana.results_dataset = copy_of_eleana_results_dataset
            self.eleana.groupsHierarchy = copy_of_eleana_groupsHierarchy
            self.eleana.notes = copy_of_eleana_notes
            self.eleana.selections = copy_of_eleana_selections
            self.eleana.static_plots = copy_of_eleana_static_plots
            return None

    # Import EPR
    def loadElexsys(self) -> object:
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('Elexsys DTA', '*.DTA'),
            ('Elexsys DSC', '*.DSC'),
            ('Elexsys YGF', '*.YGF'),
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

    def loadEMX(self):
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('EMX', '*.spc'),
            ('All files', '*.*')
        )
        filenames = filedialog.askopenfilenames(initialdir=path, filetypes=filetypes)
        if len(filenames) == 0:
            return
        for file in filenames:
            spectrum = createFromEMX(file)
            self.eleana.dataset.append(spectrum)
        last_import_dir = Path(filenames[-1]).parent
        self.eleana.paths['last_import_dir'] = last_import_dir
        return

    def loadMagnettech(self, mscope):
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('Magnettech 1', '*.spe'),
            ('All files', '*.*')
        )
        filenames = filedialog.askopenfilenames(initialdir=path, filetypes=filetypes)
        if len(filenames) == 0:
            return
        for file in filenames:
            spectrum = createFromMagnettech(file, mscope = mscope)
            self.eleana.dataset.append(spectrum)
        last_import_dir = Path(filenames[-1]).parent
        self.eleana.paths['last_import_dir'] = last_import_dir
        return

    def loadShimadzuSPC(self):
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('Shimadzu', '*.spc'),
            ('All files', '*.*')
        )
        filenames = filedialog.askopenfilenames(initialdir=path, filetypes=filetypes)
        if len(filenames) == 0:
            return
        for file in filenames:
            spectrum = createFromShimadzuSPC(file)
            self.eleana.dataset.append(spectrum)
        last_import_dir = Path(filenames[-1]).parent
        self.eleana.paths['last_import_dir'] = last_import_dir
        return

    def loadAscii(self, master, clipboard = None):
        def _create_headers(amount):
            alphabet = list(string.ascii_uppercase)
            current_len = len(alphabet)
            if current_len >= amount:
                alphabet = alphabet[:amount]
                return alphabet
            alpha_list = []
            headers = []
            for i in alphabet:
                char = list(string.ascii_uppercase)
                for each in char:
                    new_entry = i + each
                    headers.append(new_entry)
                    current_len += 1
                    if current_len >= amount:
                        alphabet.extend(headers)
                        return alphabet
            alphabet.extend(headers)
            return alphabet

        if clipboard == None:
            path = self.eleana.paths['last_import_dir']
            filetypes = (
                ('CSV file', '*.csv'),
                ('Data file', '*.dat'),
                ('Text file', '*.txt'),
                ('All files', '*.*'),)
            filename = filedialog.askopenfilename(initialdir=path, filetypes=filetypes)
            if not filename:
                return
            preview = AsciFilePreview(master = master, filename=filename, eleana = self.eleana)
            response = preview.get()
            last_import_dir = Path(filename).parent
            self.eleana.paths['last_import_dir'] = last_import_dir
        else:
            preview = AsciFilePreview(master=master, filename=None, clipboard = clipboard, eleana = self.eleana)
            response = preview.get()
            filename = None

        if response == None:
            return

        # Set separator
        r_sep = response['separator']
        if r_sep == 'Tab':
            separator = '\t'
        elif r_sep == 'Semicolon':
            separator = ';'
        elif r_sep == 'Comma':
            separator = ','
        elif r_sep == 'Space':
            separator = ' '
        else:
            separator = r_sep

        try:
            text = response['text']
            text_trimmed = text.strip()
            precision = 8
            if not separator == ',':
                text_trimmed = text_trimmed.replace(',', '.')
            df = pandas.DataFrame([list(map(lambda x: round(float(x), precision), row.split(separator))) for row in text_trimmed.split('\n')])
            df = df.map(lambda x: round(float(x), precision)).astype(object)
            headers = response['headers']
            headers = headers.strip()
            headers = headers.split(',')
            nr_of_columns = df.shape[1]
            if nr_of_columns != len(headers):
                headers = _create_headers(nr_of_columns)
            df.columns = headers
        except:
            info = CTkMessagebox(title='Error',
                                 message="Cannot import data from ASCII file. Possible reasons:\n- Your data contains non-numeric values.\n- The selected column separator does not match the separator used in the file.",
                                 icon="cancel")
            return {'Error':True}

        name = response['name']
        if name == "" or name is None:
            if filename != None:
                name = Path(filename).name
            else:
                name = ''
        spreadsheet = CreateFromTable(self.eleana, master, df=df, name=name, group = self.eleana.selections['group'])
        response = spreadsheet.get()

    def loadAdaniDat(self):
        path = self.eleana.paths['last_import_dir']
        filetypes = (
            ('Adani dat', '*.dat'),
            ('All files', '*.*'),)
        filenames = filedialog.askopenfilenames(initialdir=path, filetypes=filetypes)
        if len(filenames) == 0:
            return
        error_list = []
        for filename in filenames:
            filepath = Path(filename)
            try:
                spectrum = createFromAdaniDat(filename)
                self.eleana.dataset.append(spectrum)
                last_import_dir = filepath.parent
                self.eleana.paths['last_import_dir'] = last_import_dir
            except:
                 error_list.append(filepath.name)
        if len(error_list) == 0:
            return
        list = ', '.join(error_list)
        error = CTkMessagebox(title='Error',
                              message=f"Cannot load data from {list}.", icon="cancel")

class Save:
    def __init__(self, eleana):
        self.eleana = eleana

    @classmethod
    # def save_preferences(cls, eleana, app, grapher):
    #     ''' Save graph preferences in .EleanaPy/preferences.pic '''
    #     try:
    #         # Create object to store preferences
    #         preferences = Preferences(app, grapher)
    #         # Save current settings:
    #         filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'preferences.pic')
    #         with open(filename, 'wb') as file:
    #             pickle.dump(preferences, file)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return None

    # @classmethod
    # def save_settings_paths(cls, eleana):
    #     ''' Save settings in .EleanaPy/paths.pic '''
    #     try:
    #         # Save current settings:
    #         filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')
    #         content = eleana.paths
    #         with open(filename, 'wb') as file:
    #             pickle.dump(content, file)
    #         return True
    #     except Exception as e:
    #         Error.show(info="Cannot save settings", details=e)
    #         return None
    #
    #
    # def save_eleana_paths(self, show_error=False):
    #     '''Save self.eleana.paths to .EleanaPy user folder'''
    #     try:
    #         filename = Path(self.eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')
    #         content = self.eleana.paths
    #         with open(filename, 'wb') as file:
    #             pickle.dump(content, file)
    #     except Exception as e:
    #         if show_error:
    #             Error.show(info = "Cannot save config paths.pic file", details = e)

    def save_project(self, save_current=False):
        ''' Save project to a file '''
        init_dir = Path(self.eleana.paths.get('last_project_dir', Path.home()))
        if not save_current:
            filename = asksaveasfile(
                initialdir=init_dir,
                initialfile='',
                defaultextension=".ele",
                filetypes=[("Eleana project", "*.ele"),("All Files", "*.*")]
            )
            if not filename:
                return None
            filename = Path(filename.name)
        else:
            filename = Path(save_current)
        working_folder = Path(filename.parent, '~eleana_project.tmp')
        if working_folder.exists():
            try:
                shutil.rmtree(working_folder)
            except Exception as e:
                Error.show(info="Cannot create the project file", details=e)
                return None
        try:
            working_folder.mkdir(parents=True)
        except Exception as e:
            Error.show(info="Cannot create the project file", details=e)
            return None
        project_information = {'project version':'1.0'}
        project_to_save = Project_1(self.eleana)
        working_filename = Path(working_folder, 'project_1')
        working_information = Path(working_folder, 'info.txt')
        try:
            with open(working_filename, 'wb') as file:
                pickle.dump(project_to_save, file)
            with open(working_information, 'w') as file:
                json.dump(project_information, file)
        except Exception as e:
            message = 'Could not save the file.'
            message = message + f'\n\nDetails:\n{e}'
            info = CTkMessagebox(title="Error", message=message, icon='cancel')
        del project_to_save
        # Create zip file form the directory
        try:
            working_folder = Path(working_folder)
            path_to_folder = Path(filename.parent)
            zip_file = Path(path_to_folder, ('~' + str(filename.name[:-4] + '_tmpProject')))
            project_zip = shutil.make_archive(zip_file, 'zip', working_folder)
            project_zip = Path(project_zip)
            project_ele = project_zip.rename(filename)
        except Exception as e:
            Error.show(info="Error while creating project archive.", details=e)
            return None
        try:
            shutil.rmtree(working_folder)
        except Exception as e:
            Error.show(info="Cannot remove temporary project folder. Please remove it manually.", details=e)
            return None
        return filename

class Export:
    def __init__(self, eleana):
        self.eleana = eleana
    def csv(self, which = 'first', filename=None):
        if filename == None:
            if which == 'first' and self.eleana.selections['first'] < 0:
                info = CTkMessagebox(title="Info ", message=f'Please select data in {which}')
                return
            init_dir = self.eleana.paths.get('last_export_dir', Path("~").expanduser())
            try:
                filename = asksaveasfile(initialdir=init_dir,
                                         initialfile='',
                                         defaultextension=".csv",
                                         filetypes=[("Comma separated values", "*.csv"),
                                                    ("All Files", "*.*")
                                                    ])
                self.eleana.paths['last_export_dir'] = str(Path(filename.name).parent)
                filename = Path(filename.name)

            except:
                return {'error': True, 'desc': f'Could not save {filename} file.'}
            index = self.eleana.selections[which]
        else:
            index = which
        # Prepare data from First or second

        data = self.eleana.dataset[index]
        if data.type == 'stack 2D' and not data.complex:
            x = data.x
            y = data.y
            stk_names = data.stk_names
            name_x = data.parameters.get('name_x', 'X') + " [" + data.parameters.get('unit_x', 'a.u.') + "]"
            header = name_x
            for stk in stk_names:
                header = header + ", " + stk
            try:
                with open(filename, 'a') as exported_csv:
                    exported_csv.write(header)
                    i = 0
                    while i < len(x):
                        x_row = "\n" + str(x[i])
                        j = 0
                        data = ''
                        while j < len(stk_names):
                            data = data + ", " + str(y[j][i])
                            row = x_row + data
                            j += 1
                        exported_csv.write(row)
                        i += 1
            except:
                return {'error': True, 'desc': f'Could not save {filename.name} file.'}
            pass
        elif data.type == 'stack 2D' and data.complex:
            info = CTkMessagebox(title="Info ", message=f'Stack of complex data is not supported yet.')
            return
        elif data.type != 'stack 2D' and data.complex:
                x = data.x
                y = data.y
                re_y = np.real(y)
                im_y = np.imag(y)
                magn = np.absolute(y)
                name_x = data.parameters.get('name_x', 'X') + " [" + data.parameters.get('unit_x', 'a.u.') + "]"
                name_rey = data.parameters.get('name_y', 'Y') + " [" + data.parameters.get('unit_y', 'a.u') + "]:REAL"
                name_imy = data.parameters.get('name_y', 'Y') + " [" + data.parameters.get('unit_y', 'a.u') + "]:IMAGINARY"
                name_magn = data.parameters.get('name_y', 'Y') + " [" + data.parameters.get('unit_y', 'a.u') + "]:MAGNITUDE"
                header = str(name_x) + ", " + str(name_rey) + ", " + str(name_imy) + ", " + str(name_magn)
                try:
                    with open(filename, 'a') as exported_csv:
                        exported_csv.write(header)
                        i = 0
                        while i < len(x):
                            row = "\n" + str(x[i]) + ", " + str(re_y[i]) + ", " + str(im_y[i]) + ", " + str(magn[i])
                            exported_csv.write(row)
                            i += 1
                except:
                    return {'error': True, 'desc': f'Could not save {filename.name} file.'}

        else:
            # Single Data not complex
            x = data.x
            y = data.y
            name_x = data.parameters.get('name_x', 'X') + " [" + data.parameters.get('unit_x', 'a.u.') + "]"
            name_y = data.parameters.get('name_y', 'Y') + " [" + data.parameters.get('unit_y', 'a.u') + "]"
            header = str(name_x) + ", " + str(name_y)
            with open(filename, 'a') as exported_csv:
                exported_csv.write(header)
                i = 0
                while i < len(x):
                    row = "\n" + str(x[i]) + ", " + str(y[i])
                    exported_csv.write(row)
                    i += 1

    def group_csv(self, group):
        directory = filedialog.askdirectory()
        try:
            if directory:
                directory_path = Path(directory)
                if not directory_path.exists():
                    directory_path.mkdir(parents=True, exist_ok=True)
        except:
            info = CTkMessagebox(title='Error', message='Could not open the directory for saving data. Check permissions.')
            return
        list_of_data = self.eleana.assignmentToGroups.get(group, [])
        if not list_of_data:
            info = CTkMessagebox(title='Empty group', message=f'In the selected group: {group} there is nothing to export.')
            return
        if len(list_of_data) > 9 and len(list_of_data) < 100:
            change = 'two'
        else:
           change = 'no'
        list_of_filenames = []
        for each in list_of_data:
            name = self.eleana.dataset[each].name_nr
            entry = name.split('. ')
            name = entry[1]
            number = int(entry[0])
            if change == 'two' and number < 10:
                number = '0' + str(number)
            else:
                number = str(number)
            name = '' + number + '_' + name
            name = (name.replace('. ', '-').replace(' ', '_').replace('*', '_').replace('\\', '_').replace('/','_').replace(':', '_').replace('?', '_').replace('"', '_'))+'.csv'
            filename = Path(directory_path, name)
            list_of_filenames.append(filename)

        i = 0
        for each in list_of_filenames:
            which = list_of_data[i]
            self.csv(which = which, filename = each)
            i += 1

# class Project_1:
#     ''' Create object used to save/load Eleana projects ver. 1'''
#     def __init__(self, eleana):
#         self.dataset = eleana.dataset
#         self.results_dataset = eleana.results_dataset
#         self.groupsHierarchy = eleana.groupsHierarchy
#         self.notes = eleana.notes
#         self.selections = eleana.selections
#        self.static_plots = eleana.static_plots
class Preferences:
    ''' This class is used to create preferences'''
    def __init__(self, app, grapher):
        # Define App settings
        self.gui_appearence = app.gui_appearence
        self.color_theme = app.color_theme

        # Define Grapher settings
        self.style_first = grapher.style_first
        self.style_second = grapher.style_second
        self.style_result = grapher.style_result
        self.plt_style = grapher.plt_style
