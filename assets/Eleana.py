# Import Python Modules
import sys
import numpy as np
from pathlib import Path
import tempfile

DEVEL = True

class Eleana:
    # Main attributes associated with data gathered in the programe
    def __init__(self, version, devel):
        self.version = version
        self.dataset = []                               # <-- This variable keeps all spectra available in Eleana. It is a list of objects
        self.results_dataset = []                       # <-- This keeps data containing results
        self.assignmentToGroups = {'<group-list/>': ['All']} # <-- This keeps information about which data from dataset is assigned to particular group
        self.groupsHierarchy = {}                       # <-- This store information about which group belongs to other
        self.static_plots = []                          # This contains a list of created simple static plots
        self.active_static_plot_windows = []
        self.devel_mode = devel

        # Attribute "notes" contains general notes edited by Edit --> Notes in RTF
        self.notes = ""

        # Attribute paths contains paths for different standard directories like user, tmp, last import directory etc.
        self.paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'last_import_dir': '',
             'last_project_dir': '',
             'last_projects': [],
             'last_export_dir':''
             }

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
        self.color_span = {'color': 'gray',
                           'alpha': 0.2,
                           'ranges': [],
                           'status':0,
                           'start':0,
                           'end':0}

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

    def notify(self, variable=None):
        for observer in self._observers:
            observer.update(self, variable=variable)

    # Setter for attributes that should be observed ---
    def set_selections(self, variable=None, value=None):
        if variable == None or value == None:
            return
        self.selections[variable] = value
        if variable == 'result' or variable == 'r_stk':
            return
        if self.notify_on:
            self.notify(variable=variable)
            if self.devel_mode:
                print('Eleana.py: Activate observer')
    # End of methods for observers --------------------

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
        


    #
    # # Write "content" to text file "filename" in temporary directory (/tmp)
    # def create_tmp_file(self, filename: str, content=""):
    #     path_to_file = Path(eleana.paths['tmp_dir'], filename)
    #     try:
    #         with open(path_to_file, "w") as file:
    #             file.write(content)
    #         return {"Error": False, 'desc': "" }
    #     except:self.spinboxFrame = self.builder.get_object('spinboxFrame', self.mainwindow)
    #     self.spinbox = self.builder.get_object('spinbox', self.mainwindow)
    #     self.spinbox.grid_remove()
    #     self.spinbox = CTkSpinbox(master=self.spinboxFrame, wait_for=0.05, command=self.ok_clicked, min_value=0,
    #                               step_value=0.02, scroll_value=0.01, start_value=1)
    #     self.spinbox.grid(column=0, row=0, sticky='ew')
    #
    #         return {"Error": True, 'desc': f"Cannot create {path_to_file}"}
    #
    # # Reading temporary "filename" text file from /tmp
    # def read_tmp_file(self, filename):
    #     path_to_file = Path(Eleana.paths['tmp_dir'], filename)
    #     with open(path_to_file) as file:
    #         file_content = file.read()
    #     return file_content
    #


if __name__ == "__main__":
    eleana = Eleana()