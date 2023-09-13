# Import Python Modules
import sys
import numpy as np
from pathlib import Path
import tempfile


#notes = {"content": "","tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [],"highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],"text white": [],"text grey": [], "text blue": [], "text green": [], "text red": []}}

class Eleana():
    # Set the most important directories for the program
    interpreter = sys.executable
    notes = {"content": "",
             "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [],
                      "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                      "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}

    paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'ui': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'subprogs': Path(Path(__file__).resolve().parent, ""),
             'last_import_dir': '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/'
             }


    # ----- Methods definition of Eleana subprogs ------

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
        print('Read tmp_file: ', path_to_file)
        with open(path_to_file) as file:
            file_content = file.read()
        return file_content  #

    # Translate DSC keys into Eleana format
    dsc2eleana = {'title':'TITL',
                'unit_x':'XUNI',
                'name_x':'XNAM',
                'unit_y':'YUNI',
                'name_y':'IRNAM',
                'unit_z':'YUNI',
                'name_z':'YNAM',
                'Compl': 'IKKF',
                'MwFreq':'MWFQ',
                'ModAmp': 'ModAmp',
                'ModFreq': 'Modfreq',
                'ConvTime': 'ConvTime',
                'SweepTime': 'SweepTime',
                'Tconst':'TimeConst',
                'Resonat':'RESO',
                'Power':'MWPW',
                'PowAtten':'PowerAtten'
                }
# Class for creating data objects

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
                'Power': 'Power',
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
                self.parameters[key] = value
            except:
                pass

        print(self.parameters)
        exit()
        self.x = np.array(x_axis)
        self.y = np.array(dta)

if __name__ == "__main__":
    pass