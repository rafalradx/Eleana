from pathlib import Path, PurePath
import numpy as np
import re
class GeneralDataTemplate():
    # DSC from Bruker Elexsys

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
    comment = ''

    parameters = {'title': '',
                  'unit_x': 'G',
                  'name_x': 'Magnetic field',
                  'name_y': 'Amplitude',
                  'MwFreq': '',
                  'ModAmp': '',
                  'ModFreq': '',
                  'ConvTime': '',
                  'SweepTime': '',
                  'TimeConst': '',
                  'RESO': 'Resonator',
                  'Power': '',
                  'PowerAtten': 'PowAtten',
                  'stk_names': []
                  }
class Spectrum_CWEPR(GeneralDataTemplate):

    def __init__(self, name, x_axis: list, dta: list, dsc: dict):
        self.x = x_axis
        self.y = dta
        self.name = name
        self.complex = False
        self.type = 'single 2D'
        self.origin = 'CWEPR'

        fill_missing_keys =['title','MwFreq','ModAmp','ModFreq','SweepTime','ConvTime','TimeConst','Power','PowAtten']
        working_par = self.parameters
        for key in fill_missing_keys:
            try:
                bruker_key = GeneralDataTemplate.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                value_txt = value_txt.replace("'", "")
                working_par[key] = value_txt
            except:
                pass
        self.parameters = working_par
        self.x = np.array(x_axis)
        self.re_y = np.array(dta)

class Spectra_CWEPR_stack(Spectrum_CWEPR):

    def __init__(self, name, x_axis: list, dta: list, dsc: dict, ygf):
        super().__init__(name, x_axis, dta, dsc)

        working_parameters = self.parameters
        working_parameters['stk_names'] = []

        fill_missing_keys = ['name_z', 'unit_z', 'name_x', 'unit_x', 'name_y', 'unit_y']
        for key in fill_missing_keys:
            try:
                bruker_key = Eleana.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                value_txt = value_txt.replace("'", "")
                working_parameters[key] = value_txt
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
            name = working_parameters['name_z'] + ' ' + str(each) + ' ' + working_parameters['unit_z'] + ''
            working_parameters['stk_names'].append(name)

        self.y = list_of_y_array
        self.type = 'stack 2D'
        self.complex = False
        self.origin = 'CWEPR'
        self.parameters =working_parameters

class Spectrum_complex(GeneralDataTemplate):
    def __init__(self, name, x_axis: list, dta: list, dsc: dict):
        length = len(dta)

        y = np.array([])
        i = 0
        while i < length:
            complex_nr = complex(dta[i], dta[i+1])
            y = np.append(y, complex_nr)
            i += 2

        working_parameters = self.parameters
        fill_missing_keys = ['name_z', 'unit_z', 'name_x', 'unit_x', 'name_y', 'unit_y']
        for key in fill_missing_keys:
            try:
                bruker_key = Eleana.dsc2eleana[key]
                value = dsc[bruker_key]
                value = value.split(' ')
                value_txt = value[0]
                value_txt = value_txt.replace("'", "")
                working_parameters[key] = value_txt
            except:
                pass
        self.parameters = working_parameters
        self.y = y
        self.x = x_axis
        self.name = name
        self.complex = True
        self.type = 'single 2D'
        self.origin = 'Pulse EPR'

# Functions to import data

def createFromElexsys(filename: str) -> object:
    elexsys_DTA = Path(filename[:-3]+'DTA')
    elexsys_DSC = Path(filename[:-3]+'DSC')
    elexsys_YGF = Path(filename[:-3]+'YGF')

    # Loading dta and dsc from the files
    # DTA data will be in Y_data
    # DSC data will be in desc_data
    # YGF (if exist) will be in ygf_data
    # errors list contain list of encountered error in loading DTA and/or DSC not YGF

    error = False
    x_data = []
    dta = []
    dsc_text = '' # Raw dsc file content
    ygf = []
    dsc = {} # Translated DSC file content to dictionary

    # Load DTA from the elexsys_DTA
    try:
        dta = np.fromfile(elexsys_DTA, dtype='>d')
    except:
        elexsys_DTA = PurePath(elexsys_DTA).name
        return {"Error":True,'desc':f"Error in loading {elexsys_DTA}"}

    # If DTA sucessfully opened then read DSC
    if error != True:
        try:
            with open(elexsys_DSC, "r") as file:
                dsc_text = file.read()
        except:
            elexsys_DSC = PurePath(elexsys_DSC).name
            return {"Error": True, 'desc': f"Error in loading {elexsys_DSC}"}

    # Check if YGF exists
    if error != True:
        if elexsys_YGF.exists() == True:
            try:
                ygf = np.fromfile(elexsys_YGF, dtype='>d')
            except:
                    error = True
                    elexsys_YGF = PurePath(elexsys_YGF).name
                    return {"Error": True, 'desc': f"Error in loading {elexsys_YGF}" }
        else:
            ygf = []

    # Extract DSC to dictionary
    # Divide into separate lines

    dsc_lines = dsc_text.split('\n')
    for i in dsc_lines:
        #element = i.split("\t")
        element = re.split(r'\s+', i.strip(), maxsplit=1)
        try:
            #dsc[element[0].upper()] = element[1]
            dsc[element[0]] = element[1]
        except:
            pass

    # Create X axis
    error = False
    try:
        points = int(dsc['XPTS'])
        x_min = float(dsc['XMIN'])
        x_wid = float(dsc['XWID'])
        step = x_wid / points
        x_axis = []
        for i in range(0, points):
            x_axis.append(i * step + x_min)

    except:
        return {'Error': True, 'desc': f'Cannot create x axis for {elexsys_DTA}'}


    # Now create object containing particular type of data

    filename = Path(filename).name
    try:
        val = dsc['EXPT']
    except:
        dsc['EXPT'] = 'none'

    if dsc['YTYP'] == 'NODATA' and dsc['EXPT'] == 'CW':
        # This will create single CW EPR spectrum
        cw_spectrum = Spectrum_CWEPR(filename[:-4], x_axis, dta, dsc)
        return cw_spectrum # <--- Return object based on Spectrum_CWEPR

    elif dsc['YTYP'] != 'NODATA' and dsc['EXPT'] == 'CW':
        cw_stack = Spectra_CWEPR_stack(filename[:-4], x_axis, dta, dsc, ygf)   # <-- This will create stacked CW EPR spectra
        return cw_stack

    elif dsc['IKKF'] != 'REAL':
        spectrum_complex = Spectrum_complex(filename[:-4], x_axis, dta, dsc)
        return spectrum_complex
