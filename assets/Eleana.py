# Import Python Modules
import gc
import sys
import numpy as np
from pathlib import Path
import tempfile
from dataclasses import dataclass, field
from typing import Dict, Any
import pickle
from Error import Error
import shutil
import json
from tkinter.filedialog import asksaveasfile, askopenfilename
import gc
from modules.CTkMessagebox import CTkMessagebox

@dataclass
class GuiState:
    autoscale_x: bool
    autoscale_y: bool
    log_x: bool
    log_y: bool
    indexed_x: bool
    cursor_mode: str
    inverted_x: bool

@dataclass
class Settings:
    general: Dict[str, Any] # Store general settings for GUI
    grapher: Dict[str, Any] # Settings associated with grapher

@dataclass
class Storage:
    subprog_settings: Dict[str, Any]
    additional_plots: list[Any]
    static_plots: list[Any]
    active_static_plot_windows: list[Any]
    cursor_annotations: list[Any]

@dataclass
class Project_1:
    dataset: list[object]
    results_dataset: list[object]
    groupsHierarchy: dict
    notes: str
    selections: Dict[str, Any]
    static_plots: list

class Eleana:
    # Main attributes associated with data gathered in the programe
    def __init__(self, version, devel):
        self.devel_mode = devel
        self.version = version
        self.initialize()

    def initialize(self):
        self.busy = False                               # <-- This variable is set to True if something is triggered in application and other proces must wait until it is False
        self.dataset = []                               # <-- This variable keeps all spectra available in Eleana. It is a list of objects
        self.results_dataset = []                       # <-- This keeps data containing results
        self.assignmentToGroups = {'<group-list/>': ['All']} # <-- This keeps information about which data from dataset is assigned to particular group
        self.groupsHierarchy = {}                       # <-- This store information about which group belongs to other
        self.cmd_error = ''                             # This contains the current error for command line

        # Attribute "notes" contains general notes edited by Edit --> Notes in RTF
        self.notes = ""

        # Attribute paths contains paths for different standard directories like user, tmp, last import directory etc.
        self.paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent.parent, "pixmaps"),
             'last_import_dir': '',
             'last_project_dir': '',
             'last_projects': [],
             'last_export_dir':''
             }
        # Load saved paths
        try:
            self.load_paths()
        except:
            pass

        # Attribute selection is the basic storage of the settings obtained from states in GUI
        # Description:
        # group  --> The name of selected group in Group combobox in object: app.sel_group
        #
        # first \
        # second )-->  integer containing index in Eleana.dataset which is selected by comboboxes app.sel_first, app.sel_second, app.sel_result
        # result/
        #
        # f_cpl\
        # s_cpl )--> ONLY FOR COMPLEX DATA. Defines how complex data should be used for graph, calculation, etc.
        # r_cpl/     Can be set to:
        #                           empty or re - show real part
        #                           im -          show imaginary part
        #                           cpl -         show both re and im
        #                           magn -        show complex magnitude

        # f_stk\
        # s_stk )--> (ONLY IF DATA IS A STACK). It is integer containing index of row for stack in y data
        # r_stk/
        #
        # f_dsp\
        # s_dsp )--> Can be True or False. If false then the spectrum selected is not displayed on graph by data is selected
        # r_dsp/

        self.selections = {'group':'All',
                      'first':-1, 'second':-1, 'result':-1,
                      'f_cpl':'re','s_cpl':'re', 'r_cpl':'re',
                      'f_stk':0, 's_stk':0, 'r_stk':0,
                      'f_dsp':True, 's_dsp':True ,'r_dsp':True
                      }

        # Create observer list
        self._observers = []
        self.notify_on = False

        # Define ranges for setting color span
        #       color - defines the color of the selection
        #       alpha - defines transparency level
        #       ranges - contain min and max of selected ranges
        #       status - is the current clicking operations: 0 - wait for first click
        #                                                    1 - first X point was clicked
        #


        # Storage for settings for subprogs
        # The structure is list of dicts. Dicts has structure:
        # {'subprog':'SUBPROG_PYTHON_FILENAME', 'content':[LIST_OF_DICTS_CONTAINING_STORAGE]}


        # Create contener for guistate
        self.gui_state = GuiState(  autoscale_x = True,
                                    autoscale_y = True,
                                    log_x = False,
                                    log_y = False,
                                    indexed_x = False,
                                    cursor_mode = 'None',
                                    inverted_x = False,

                                    )

        # Create temporary storages
        self.storage = Storage(subprog_settings = {},
                               static_plots = [],
                               active_static_plot_windows = [],
                               additional_plots = [],
                               cursor_annotations = []
                               )

        # Try loading saved settings
        self.settings = self.load_settings()
        #self.settings = None
        if self.settings is None:
            self.set_default_settings()
            # Save settings on disk
            self.save_settings()

    def reset(self):
        self._observers.clear()
        self.dataset.clear()
        self.results_dataset.clear()
        self.gui_state = None
        self.settings = None
        self.storage = None
        gc.collect()
        self.__init__(version = self.version, devel = self.devel_mode)

    ''' ***************************** 
     *         OBSERVER METHODS      *
     ******************************'''
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, variable=None, value=None):
        for observer in self._observers:
            observer.update(self, variable=variable, value=value)

    # Setter for attributes that should be observed ---
    def set_selections(self, variable=None, value=None):
        if variable == None or value == None:
            return
        if variable == 'grapher_action':
            if self.notify_on:
                self.notify(variable=variable, value=value)
            return
        self.selections[variable] = value
        if variable == 'result' or variable == 'r_stk':
            return
        if self.notify_on:
            self.notify(variable=variable, value=value)
            #if self.devel_mode:
            #    print('Eleana.py: Activate observer')

    # End of methods for observers --------------------
    def set_default_settings(self):
        ''' Set default settings '''

        # Default general settings
        grapher = {}
        general = {'gui_appearance': 'dark',
                   'color_theme': 'dark-blue'}
        # Settings for Grapher
        grapher['cursor_modes'] = [
            {'label': 'None', 'hov': False, 'a_txt': False, 'annot': False, 'multip': False, 'store': False},
            {'label': 'Continuous read XY', 'hov': True, 'a_txt': True, 'annot': True, 'multip': False, 'store': False},
            {'label': 'Selection of points with labels', 'hov': False, 'annot': True, 'a_txt': True, 'multip': True,
             'store': True},
            {'label': 'Selection of points', 'hov': False, 'annot': True, 'a_txt': False, 'multip': True,
             'store': True},
            {'label': 'Numbered selections', 'hov': False, 'annot': True, 'a_txt': True, 'multip': True, 'store': True,
             'nr': True},
            {'label': 'Free select'},
            {'label': 'Crosshair', 'hov': True, 'a_txt': True, 'annot': True, 'multip': False, 'store': False},
            {'label': 'Range select', 'hov': False, 'annot': True, 'a_txt': True, 'multip': True, 'store': True,
             'nr': True}
        ]
        grapher['style_of_annotation'] = {
            'text': "",
            'number': True,
            'xytext': (0.03, 0.03),
            'arrowprops': {
                "arrowstyle": "->",  # Arrow style
                "lw": 1.5,  # Arrow thickness
                "color": "black",  # Arrow color
            },
            "bbox": {
                "boxstyle": "round",  # Rounded text field
                "fc": "orange",  # Background color
                "ec": "black",  # Border color
                "lw": 0.5  # Border thickness
            },
            "fontsize": 10,  # Font size
            "color": "black"  # Font color
        }
        grapher['plt_style'] = 'Solarize_Light2'
        grapher['style_first'] = {
            'plot_type': 'line',
            'linewidth': 2,
            'linestyle': 'solid',
            'marker': '.',
            's': 5,
            'color_re': "#d53422",
            'color_im': "#ef6f74"
        }
        grapher['style_second'] = {
            'plot_type': 'line',
            'linewidth': 2,
            'linestyle': 'solid',
            's': 5,
            'marker': '.',
            'color_re': '#008cb3',
            'color_im': '#07bbed'
        }
        grapher['style_result'] = {
            'plot_type': 'line',
            'linewidth': 2,
            'linestyle': 'solid',
            's': 5,
            'marker': '.',
            'color_re': '#108d3d',
            'color_im': '#32ab5d'
        }

        grapher['additional_plots_style'] = {
            'color': 'gray',
            'linewidth': 2,
            'linestyle': 'dashed',
        }
        grapher['color_span'] = {'color': 'gray',
                                 'alpha': 0.2,
                                 'ranges': [],
                                 'status': 0,
                                 'start': 0,
                                 'end': 0}
        grapher['custom_annotations'] = []

        # Static plots
        grapher['static_plots'] = []
        grapher['active_static_plot_windows'] = []

        # Store settings in Settings dataclass
        self.settings = Settings(general=general, grapher=grapher)

    def save_settings(self):
        """Save settings in .EleanaPy/preferences.pic"""
        try:
            filename = Path(self.paths['home_dir']) / '.EleanaPy' / 'settings.pic'
            filename.parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'wb') as file:
                pickle.dump(self.settings, file, protocol=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def save_paths(self):
        ''' Save settings in .EleanaPy/paths.pic '''
        filename = Path(self.paths['home_dir'], '.EleanaPy', 'paths.pic')
        content = self.paths
        with open(filename, 'wb') as file:
            pickle.dump(content, file, protocol=4)
        return True

    def save_project(self, save_current=False):
        ''' Save project to a file '''
        init_dir = Path(self.paths.get('last_project_dir', Path.home()))
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
        project_to_save = Project_1(dataset = self.dataset,
                                    results_dataset = self.results_dataset,
                                    groupsHierarchy = self.groupsHierarchy,
                                    notes = self.notes,
                                    selections = self.selections,
                                    static_plots = self.storage.static_plots
                                    )


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
        gc.collect()

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


        # last_projects = self.paths['last_projects']
        # saved_path_string = str(project_ele)
        # if saved_path_string in last_projects:
        #     index = last_projects.index(saved_path_string)
        #     del last_projects[index]
        # last_projects.insert(0, str(saved_path_string))
        # last_projects = last_projects[:20]
        # # Write the list to eleana.paths
        # self.paths['last_projects'] = last_projects
        # self.paths['last_project_dir'] = Path(last_projects[0]).parent
        # self.save_paths()
        # # Perform update to place the item into menu
        # return str(Path(last_projects[0]).name[:-4] + ' - Eleana')

        saved_path_string = str(project_ele)
        last_projects = list(self.paths.get('last_projects', []))  # jawna kopia

        if saved_path_string in last_projects:
            last_projects.remove(saved_path_string)
        last_projects.insert(0, saved_path_string)
        last_projects = last_projects[:20]

        self.paths['last_projects'] = last_projects
        self.paths['last_project_dir'] = Path(last_projects[0]).parent
        self.save_paths()

        return f"{Path(last_projects[0]).stem} - Eleana"

    def load_paths(self):
        ''' Load saved settings from home/.EleanaPy/paths.pic'''
        filename = Path(self.paths['home_dir'], '.EleanaPy', 'paths.pic')
        # Read paths.pic
        file_to_read = open(filename, "rb")
        paths = pickle.load(file_to_read)

        self.paths['last_import_dir'] = paths['last_import_dir']
        self.paths['last_projects_dir'] = paths['last_projects_dir']
        self.paths['last_export_dir'] = paths['last_export_dir']

        file_to_read.close()
        # Create last project list in the main menu
        last_projects = self.paths['last_projects']
        last_projects = [element for i, element in enumerate(last_projects) if i <= 10]
        # Write the list to eleana.paths
        self.paths['last_projects'] = last_projects
        return True

    def load_settings(self):
        ''' Load saved graph settings from home/.EleanaPy/preferences.pic'''
        try:
            filename = Path(self.paths['home_dir'], '.EleanaPy', 'settings.pic')
            # Read paths.pic
            file_to_read = open(filename, "rb")
            preferences = pickle.load(file_to_read)
            file_to_read.close()
            return preferences
        except Exception as e:
            print(e)
            self.set_default_settings()
            return None

    #
    # Operations on dataset
    #

    def name_nr_to_index(self, selected_value_text):
        ''' Returns index of Eleana.dataset which name_nr attribute is equal to argument: selected_value_text'''
        numbered_names = []
        for each in self.dataset:
            numbered_names.append(each.name_nr)
        if selected_value_text in numbered_names:
            index = numbered_names.index(selected_value_text)
            return index

    def get_index_by_name(self, selected_value_text):
        ''' Function returns index in dataset of spectrum
            having the name_nr '''
        i = 0
        while i < len(self.dataset):
            name = self.dataset[i].name_nr
            if name == selected_value_text:
                return i
            i += 1
    def get_indexes_from_group(self):
        ''' Return list of indexes in self.dataset
            that belongs to the current group '''
        indexes = []
        group = self.selections['group']
        if group == 'All':
            for data in self.dataset:
                index = self.get_index_by_name(data.name_nr)
                indexes.append(index)
        else:
            indexes = self.assignmentToGroups[group]
        return indexes

    def getDataFromSelection(self, first_second_or_results: str):
        '''Returns X, reY, imY and boolean complex depending on values in self.selections
           Argument first_second_or_results is string 'first' for First selection
                                                      'second' for Second selection
                                                      'result' for Results selection
        '''
        ''' This function is used to plot the data on graph not calculations '''
        selection = self.selections
        if first_second_or_results == 'first':
            index_main = selection['first']     # Get index from dataset
            index_stk = selection['f_stk']      # Get index in stack if it is a stack
            show_complex = selection['f_cpl']   # If complex then how it should be displayed

        elif first_second_or_results == 'second':
            index_main = selection['second']
            index_stk = selection['s_stk']
            show_complex = selection['s_cpl']

        elif first_second_or_results == 'result':
            index_main = selection['result']
            index_stk = selection['r_stk']
            show_complex = selection['r_cpl']
        else:
            return {}

        if first_second_or_results == 'result':
            data = self.results_dataset[index_main]
        else:
            data = self.dataset[index_main]

        type = data.type

        if type == 'stack 2D':
            y = data.y[index_stk]

        # If data is complex
        if data.complex:
            x = data.x
            if show_complex == 'im':
                im_y = [value.imag for value in data.y]
                re_y = np.array([])
                if type == 'stack 2D':
                    im_y = im_y[index_stk]
            elif show_complex == 'cpl':
                re_y = [value.real for value in data.y]
                im_y = [value.imag for value in data.y]
                if type == 'stack 2D':
                    re_y = re_y[index_stk]
                    im_y = im_y[index_stk]
            elif show_complex == 'magn':
                re_y = np.real(data.y)
                im_y = np.imag(data.y)
                magnitude = (re_y**2+im_y**2)**0.5
                im_y = np.array([])
                re_y = np.array(magnitude)
                if type == 'stack 2D':
                   re_y = re_y[index_stk]
            else:
                re_y = [value.real for value in data.y]
                im_y = np.array([])
                if type == 'stack 2D':
                    re_y = re_y[index_stk]
            return {'x':x, 're_y':re_y, 'im_y':im_y, 'complex':True}

        # Data is not complex
        else:
            x = data.x
            y = data.y
            if type == 'stack 2D':
                y = data.y[index_stk]
        return {'x':x, 're_y':y, 'complex':False, 'im_y':np.array([])}

    def data_from_selected_range(self, which='first'):
        # Gets x and y data from the range selected in graph
        x = None
        y = None
        index_in_dataset = self.selections[which]
        if index_in_dataset == -1:
            return x,y
        data = self.dataset[index_in_dataset]
        x = data.x
        y = data.y
        type = data.type


if __name__ == "__main__":
    eleana = Eleana()