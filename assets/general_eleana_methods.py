# Import Python Modules
import sys
import numpy as np
from pathlib import Path
import tempfile

class Eleana():
    # Main attributes associated with data gathered in the programe
    interpreter = sys.executable # <-- Python version for subprocesses
    dataset = []            # <-- This variable keeps all spectra available in Eleana. It is a list of objects
    results_dataset = []    # <-- This keeps data containing results
    assignmentToGroups = {} # <-- This keeps information about which data from dataset is assigned to particular group
    groupsHierarchy = {}    # <-- This store information about which group belongs to other

    # Attribute "notes" contains general notes edited by Edit --> Notes in RTF
    notes = {"content": "",
             "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [],
                      "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                      "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}

    # Attribute paths contains paths for different standard directories like user, tmp, last import directory etc.
    paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'ui': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'assets': Path(Path(__file__).resolve().parent, ""),
             'last_import_dir': '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/'
             }

    # Attribute selection is the basic storage of the settings obtainted from states in GUI
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
    selections = {'group':'All',
                  'first':0, 'second':0, 'result':0,
                  'f_cpl':'','s_cpl':'', 'r_cpl':'',
                  'f_stk':0, 's_stk':'', 'r_stk':'',
                  'f_dsp':True, 's_dsp':True ,'r_dsp':True
                  }

    # --- Dictionaries translation different par files to Eleana format ---
    # Translation for DSC from Bruker Elexsys
    dsc2eleana = {'title': 'TITL',
                  'unit_x': 'XUNI',
                  'name_x': 'XNAM',
                  'unit_y': 'YUNI',
                  'name_y': 'IRNAM',
                  'unit_z': 'YUNI',
                  'name_z': 'YNAM',
                  'Compl': 'IKKF',
                  'MwFreq': 'FrequencyMon',
                  'ModAmp': 'ModAmp',
                  'ModFreq': 'ModFreq',
                  'ConvTime': 'ConvTime',
                  'SweepTime': 'SweepTime',
                  'Tconst': 'TIMEC',
                  'Reson': 'RESO',
                  'Power': 'Power',
                  'PowAtten': 'PowerAtten'
                  }

    # Translation for Bruker EMX
    parEMX2elena = {}




    # ----- METHODS ------
    # def add_numbers_to_dataset(self):
    #     names = []
    #     i = 0
    #     for data in self.dataset:
    #         name = str(i+1) + '. ' + data.name
    #         self.dataset[i].name = name
    #         i += 1



    # Write "content" to text file "filename" in temporary directory (/tmp)
    def create_tmp_file(self, filename: str, content=""):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        try:
            with open(path_to_file, "w") as file:
                file.write(content)
            return {"Error": False, 'desc': "" }
        except:
            return {"Error": True, 'desc': f"Cannot create {path_to_file}"}
    # Reading temporary "filename" text file from /tmp
    def read_tmp_file(self, filename):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        with open(path_to_file) as file:
            file_content = file.read()
        return file_content  #


# --- Classes for Construction Data Objects ---
class GeneralDataTemplate():
    # Name of the data
    name = ''

    # The number and name ex. 2. CW-EPR_heme_bL
    name_nr = ''

    # Names of groups to which this data belongs
    groups = ['All']

    # If spectrum is complex numbers set to TRUE
    complex = False

    # This defines data type: '2D_stack'
    # Empty or  'single 2D'  - single 2D spectrum
    #           'stack 2D' - stack of 2D spectra
    type = ''

    # Optional - origin specifies how the spectrum was created: for example CWEPR
    origin = ''

    # Contains various comments
    comments = Eleana.notes

    def plotData(self, first_second_or_results: str):
        # This method reurns X, reY, imY and boolean complex depending on values in eleana.selections
        # Argument first_second_or_results is string 'first' for Sirst selection
        #                                            'second' for Second selection
        #                                            'result' for Results selection

        selection = Eleana.selections
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
            print("Wrong argument. Must be 'first', 'second' or 'result'")
            return {}

        data = Eleana.dataset[index_main]
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
                re_y = data.y.abs()
                im_y = np.array([])
                if type == 'stack 2D':
                   re_y = re_y[index_stk]
            else: # show_complex == 're' or ''
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


class Spectrum_CWEPR(GeneralDataTemplate):     # Class constructor for single CW EPR data

    parameters = {'title':'',
                'unit_x':'G',
                'name_x':'Magnetic field',
                'name_y':'Amplitude',
                'MwFreq':'',
                'ModAmp':'',
                'ModFreq':'',
                'ConvTime':'',
                'SweepTime':'',
                'TimeConst':'',
                'RESO': 'Resonator',
                'Power': '',
                'PowerAtten': 'PowAtten'
                }
    def __init__(self, name, x_axis: list, dta: list, dsc: dict):
        self.x = x_axis
        self.y = dta
        self.name = name
        self.complex = False
        self.type = 'single 2D'
        self.origin = 'CWEPR'

        fill_missing_keys =['title','MwFreq','ModAmp','ModFreq','SweepTime','ConvTime','TimeConst','Power','PowAtten']
        for key in fill_missing_keys:
            try:
                bruker_key = Eleana.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                value_txt = value_txt.replace("'", "")
                self.parameters[key] = value_txt
            except:
                pass

        self.x = np.array(x_axis)
        self.re_y = np.array(dta)

class Spectra_CWEPR_stack(Spectrum_CWEPR):

    def __init__(self, name, x_axis: list, dta: list, dsc: dict, ygf):
        super().__init__(name, x_axis, dta, dsc)
        self.name = name
        self.x_axis = x_axis
        self.dta = dta
        self.dsc = dsc
        self.ygf = ygf
        parameters = self.parameters
        parameters['stk_names'] = []

        fill_missing_keys = ['name_z', 'unit_z']
        for key in fill_missing_keys:
            try:
                bruker_key = Eleana.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                value_txt = value_txt.replace("'", "")
                parameters[key] = value_txt
            except:
                pass

        # Divide y into list of spectra amplitudes:
        length_of_one = len(x_axis)
        list_of_y = []
        i = 0
        while i < len(ygf):
            spectrum = dta[i*length_of_one:(i+1)*length_of_one]
            list_of_y.append(spectrum)
            i += 1

        list_of_y_array = np.array(list_of_y)

        # Create in stack names:
        for each in ygf:
            name = parameters['name_z'] + ' ' + str(each) + ' ' + parameters['unit_z'] + ''
            parameters['stk_names'].append(name)

        self.y = list_of_y_array
        self.type = 'stack 2D'
        self.complex = False
        self.origin = 'CWEPR'


class Spectrum_complex(GeneralDataTemplate):
    def __init__(self, name, x_axis: list, dta: list, dsc: dict):
        #super().__init__(name, x_axis, dta, dsc)
        self.name = name
        self.x_axis = x_axis
        self.dta = dta
        self.dsc = dsc

        length = len(dta)/2
        reY = []
        imY = []

        i = 0
        while i < length:
            reY.append(dsc[i])
            imY.append(dsc[i+1])
            i += 1

        self.y = reY + 1j * imY


class Update():

    def dataset_list(self) -> list:
        # This function is used to create list of data for all
        names_numbered = ['None']
        i = 0
        for data in Eleana.dataset:
            number = str(i+1)
            name_number = number + '. ' + data.name
            names_numbered.append(name_number)
            i += 1

        i = 0
        while i < len(Eleana.dataset):
            Eleana.dataset[i].name_nr = names_numbered[i+1]
            i += 1
        #return names_numbered

    def selections_widgets(self, app: object):
        selections = Eleana.selections
        first_nr = selections['first']
        try:
            first = Eleana.dataset[first_nr]
            f_stk = selections['f_stk']
        except IndexError:
            selections['first'] = 0
            selections['f_stk'] = 0
            f_stk = selections['f_stk']

        second_nr = selections['second']
        try:
            second = Eleana.dataset[second_nr]
            s_stk = selections['s_stk']
        except IndexError:
            selections['second'] = 0
            selections['s_stk'] = 0
            s_stk = selections['s_stk']

        result_nr = selections['result']
        try:
            result = Eleana.results_dataset[result_nr]
            r_stk = selections['r_stk']
        except IndexError:
            selections['result'] = 0
            selections['r_stk'] = 0

        # Show or hide widgets
        if len(Eleana.results_dataset) == 0:
            app.resultFrame.grid_remove()

        # Upadte FIRST frame
        if len(Eleana.dataset) == 0 or first.type != "stack 2D":
            app.firstStkFrame.grid_remove()
            app.firstComplex.grid_remove()

        elif first.type == "stack 2D":
            app.firstStkFrame.grid(row=2, column=0)
            app.f_stk.configure(values=first.parameters['stk_names'])
        try:
            if first.complex:
                app.firstComplex.grid()
        except:
            pass

        # Update SECOND frame
        if len(Eleana.dataset) == 0 or second.type != "stack 2D":
            app.secondStkFrame.grid_remove()
            app.secondImaginary.grid_remove()

        elif second.type == "stack 2D":
            app.secondStkFrame.grid(row=2, column=0)
            app.s_stk.configure(values=second.parameters['stk_names'])
        try:
            if second.complex:
                app.secondImaginary.grid()
        except:
            pass

        # Update RESULT frame
        if len(Eleana.results_dataset) == 0 or result.type != "stack 2D":
            app.resultStkFrame.grid_remove()
            app.resultImaginary.grid_remove()

        elif second.type == "stack 2D":
            app.resultStkFrame.grid(row=2, column=0)
            app.r_stk.configure(values=result.parameters['stk_names'])
            if result.complex:
                app.resultImaginary.grid()

    def results_list(self, results):
        names = []
        i = 1
        for data in dataset:
            name = data.name
            name = str(i) + ". " + name
            names.append(name)
            i += 1
        return names


    # Creating groups on basis of groups defined in Eleana.dataset
    def groups(self, dataset):
        found_groups = set()
        self.groups = []
        for data in dataset:
            self.groups.extend(data.groups)
        found_groups.update(self.groups)

        self.assignToGroups ={}
        for group_name in found_groups:

            i = 0
            spectra_numbers = []
            while i < len(dataset):
                groups_in_single_spectrum = dataset[i].groups
                if group_name in groups_in_single_spectrum:
                    spectra_numbers.append(i)
                i += 1
            self.assignToGroups[group_name] = spectra_numbers
        return self.assignToGroups


    def firstComobox(self, selections: dict, groups: dict):
        pass


if __name__ == "__main__":
    eleana = Eleana()