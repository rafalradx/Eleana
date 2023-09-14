# Import Python Modules
import sys
import numpy as np
from pathlib import Path
import tempfile

class Eleana():

    dataset = []
    set_result = []

    interpreter = sys.executable

    notes = {"content": "",
             "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [],
                      "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                      "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}

    # Set the most important directories for the program
    paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'ui': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'subprogs': Path(Path(__file__).resolve().parent, ""),
             'last_import_dir': '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/'
             }
    # Selections define what is the state of widgets that selsect spectra
    # group: int --> number of selected group
    # first, second, result: int --> number on combobox selector
    # f_cpl, s_cpl, r_cpl: str (ONLY FOR COMPLEX) --> selection of what is shown in the graph:
    #                                 empty or re - show real part
    #                                 im -          show imaginary part
    #                                 cpl -         show both re and im
    #                                 magn -        show complex magnitude
    # f_stk, s_stk, r_stk: int (ONLY FO STACK) --> selects subspectra in the spectra stack
    # f_dsp, s_dsp, r_dsp: bool --> if thrue then first, second and result appears in the graph, respectively

    selections = {'group':0,
                  'first':0, 'second':0, 'result':0,
                  'f_cpl':'','s_cpl':'', 'r_cpl':'',
                  'f_stk':0, 's_stk':'', 'r_stk':'',
                  'f_dsp':True, 's_dsp':True ,'r_dsp':True
                  }

    # Dictionaries for different par files to Eleana format
    # Bruker Elexsys
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

    # Bruker EMX
    parEMX2elena = {}


    # ----- METHODS ------
    # Method for saving temporary text file in file /tmp
    def create_tmp_file(self, filename: str, content=""):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        try:
            with open(path_to_file, "w") as file:
                file.write(content)
            return {"Error": False, 'desc': "" }
        except:
            return {"Error": True, 'desc': f"Cannot create {path_to_file}"}
    # Method fo reading temporary text file in /tmp
    def read_tmp_file(self, filename):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        with open(path_to_file) as file:
            file_content = file.read()
        return file_content  #


# --- DATA OBJECTS CONSTUCTORS ---

class Spectrum_CWEPR():     # Class constructor for single CW EPR data
    name = ''
    groups = []
    is_complex = False
    type = ''
    origin = ''
    comments = Eleana.notes
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
        self.groups = ['All']
        self.complex = False
        self.type = 'single 2D'
        self.origin = 'CW EPR'

        fill_missing_keys =['title','MwFreq','ModAmp','ModFreq','SweepTime','ConvTime','TimeConst','Power','PowAtten']
        for key in fill_missing_keys:
            try:
                bruker_key = Eleana.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                self.parameters[key] = value_txt
            except:
                pass

        self.x = np.array(x_axis)
        self.y = np.array(dta)

if __name__ == "__main__":
    pass