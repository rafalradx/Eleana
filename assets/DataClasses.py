
from pathlib import Path, PurePath
import numpy as np
import re
from modules.ShimadzuSPC.shimadzu_spc import load_shimadzu_spc

class Single2D:
    def __init__(self, data: dict):
        self.parameters: dict = data['parameters']
        self.groups: list = data['groups']
        self.x: np.ndarray = data['x']
        self.y: np.ndarray = data['y']
        self.name: str = data['name']
        self.complex = data.get('complex', False)
        self.type = 'single 2D'
        self.origin = data.get('origin', '')


class Spectrum_CWEPR:
    def __init__(self, name, x_axis: list, dta: list, dsc: dict, format="elexsys"):
        self.parameters = {'title': '', 'unit_x': 'G', 'name_x': 'Field', 'name_y': 'Intensity', 'MwFreq': '', 'ModAmp': '', 'ModFreq': '',
                           'ConvTime': '',  'SweepTime': '',  'TimeConst': '',  'RESO': '',  'Power': '', 'PowerAtten': ''}
        self.groups = []
        self.x = x_axis
        self.y = dta
        self.name = name
        self.name_nr = ''
        self.complex = False
        self.type = 'single 2D'
        self.origin = 'CWEPR'
        self.stk_names = []

        working_par = self.parameters

        fill_missing_keys =['title','MwFreq','ModAmp','ModFreq','SweepTime','ConvTime','TimeConst','Power','PowAtten']
        for key in fill_missing_keys:
            try:
                if format == 'elexsys':
                    working_par[key] = create_eleana_par(dsc, dsc2eleana(key))
                elif format == 'emx' or format == 'esp':
                    working_par[key] = create_eleana_par(dsc, par2eleana(key, format))
            except:
                pass

        self.parameters = working_par
        self.x = np.array(x_axis)
        self.re_y = np.array(dta)

class Spectra_CWEPR_stack(Spectrum_CWEPR):
    def __init__(self, name, x_axis: list, dta: list, dsc: dict, ygf, format='elexsys'):
        super().__init__(name, x_axis, dta, dsc)

        working_parameters = self.parameters

        fill_missing_keys = ['name_z', 'unit_z', 'name_x', 'unit_x', 'name_y', 'unit_y']
        for key in fill_missing_keys:
            try:
                if format == 'elexsys':
                    working_parameters[key] = create_eleana_par(dsc, dsc2eleana(key))
                elif format == 'emx_stack':
                    working_parameters[key] = create_eleana_par(dsc, par2eleana(key, format))
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
        working_stk_names = []
        # Create in stack names:
        for each in ygf:
            name = working_parameters.get('name_z', '') + ' ' + str(each) + ' ' + working_parameters.get('unit_z', '')
            working_stk_names.append(name)

        self.stk_names = working_stk_names
        self.y = list_of_y_array
        self.type = 'stack 2D'
        self.complex = False
        self.origin = 'CWEPR'
        self.parameters = working_parameters

class Spectrum_complex:
    def __init__(self, name, x_axis: list, dta: list, dsc: dict):
        self.parameters = {'title': '', 'unit_x': '', 'name_x': '', 'name_y': '', 'MwFreq': '', 'ModAmp': '',
                           'ModFreq': '',
                           'ConvTime': '', 'SweepTime': '', 'TimeConst': '', 'RESO': '', 'Power': '', 'PowerAtten': '',
                           'stk_names': []}
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
                bruker_key = dsc2eleana(key)
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
        self.name_nr = ''
        self.groups = ['All']
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
        element = re.split(r'\s+', i.strip(), maxsplit=1)
        try:
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

def createFromEMX(filename: str) -> object:
    emx_SPC = Path(filename[:-3] + 'spc')
    emx_PAR = Path(filename[:-3] + 'par')
    dsc = {}
    dta = []
    x_data = []
    format = {'spectr':'', 'stack':False}

    # Load PAR
    try:
       with open(emx_PAR, 'r', encoding='ascii', errors='ignore') as file:
           dsc_text = file.read()
       if re.search(r'DOS\s*Format', dsc_text):
           format['spectr'] = 'emx'
       else:
           format['spectr'] = 'esp'
    except:
        return {'Error': True, 'desc': f'Cannot load {emx_PAR}'}

    # Load SPC to dta varaiable
    try:
       with open(emx_SPC, 'rb') as file:
           binary_data = file.read()
           if format['spectr'] == 'emx':
               dta = np.frombuffer(binary_data, dtype=np.float32)
           else:
               dta = np.frombuffer(binary_data, dtype='>i4')
    except:
        return {'Error': True, 'desc': f'Cannot load {emx_SPC}'}

    # Convert Par to dictionary and store in dsc dictionary
    dsc_lines = dsc_text.split('\n')
    for i in dsc_lines:
        element = re.split(r'\s+', i.strip(), maxsplit=1)
        try:
            dsc[element[0]] = element[1]
        except:
            pass

    # Check if data contains stack or is single

    if dsc['JSS'] == '0' or format['spectr'] == 'esp':
        format['stack'] = False
    else:
        format['stack'] = True

    filename = Path(filename).name



    # Depending on the format create x axis and object with Given EPR Type
    if format['spectr'] == 'emx' and format['stack'] == False:
        # Create X axis for EMX when there is only a single spectrum
        try:
            points = int(dsc['ANZ'])
            x_min = float(dsc['GST'])
            x_wid = float(dsc['GSI'])
            step = x_wid / points
            x_axis = []
            for i in range(0, points):
                x_axis.append(i * step + x_min)
        except:
            return {'Error': True, 'desc': f'Cannot create x axis for {emx_SPC}'}
        cw_spectrum = Spectrum_CWEPR(filename[:-4], x_axis, dta, dsc, 'emx')
        return cw_spectrum

    elif format['spectr'] == 'emx' and format['stack'] == True:
        # Create x axis for EMX stack of spectra
        try:
            points = int(dsc['SSX'])
            x_min = float(dsc['XXLB'])
            x_wid = float(dsc['XXWI'])
            step = x_wid / points
            x_axis = []
            for i in range(0, points):
                x_axis.append(i * step + x_min)

            ygf = []
            z_elements = int(dsc['SSY'])
            z_elements -= 1
            z_wid = float(dsc['XYWI'])
            z_min = float(dsc['XYLB'])
            z_step = z_wid / z_elements
            if z_elements > 0 and z_wid > 0:
                z_step = z_wid / z_elements
                for i in range(z_elements):
                    ygf.append(z_min + i * z_step)

        except:
            return {'Error': True, 'desc': f'Cannot create x axis for {emx_SPC}'}
        cw_stack = Spectra_CWEPR_stack(filename[:-4], x_axis, dta, dsc, ygf, 'emx_stack')
        return cw_stack


    elif format['spectr'] == 'esp' and format['stack'] == False:
        # Create X axis for ESP if there is only a single spectrum
        try:
            points = len(dta)
            x_min = float(dsc['GST'])
            x_wid = float(dsc['HSW'])
            step = x_wid / points
            x_axis = []
            for i in range(0, points):
                x_axis.append(i * step + x_min)
        except:
            return {'Error': True, 'desc': f'Cannot create x axis for {emx_SPC}'}
        cw_spectrum = Spectrum_CWEPR(filename[:-4], x_axis, dta, dsc, 'esp')
        return cw_spectrum

    elif format['spectr'] == 'esp' and format['stack'] == True:
        # Create X axis for ESP if there is only a single spectrum
        print('DataClasses, line 284, create ESP Stack Loader')
        exit()

def createFromShimadzuSPC(filename: str) -> object:
    spectrum = load_shimadzu_spc(filename)
    if spectrum == None:
        return {'Error':True, 'desc':'Error'}

    name = Path(filename).name
    data =  {'parameters':
                {   'unit_x': 'nm',
                    'name_x': 'Wavelength',
                    'unit_y': 'OD',
                    'name_y': 'Absorbance',
                    'unit_z': ''
                },
             'groups':'All',
             'x': np.array(spectrum['x']),
             'y': np.array(spectrum['y']),
             'name': name,
             'complex': False,
             'type': 'single2D',
             'origin': 'UV VIS spectrum'
             }
    spectrum = Single2D(data)
    return spectrum



def create_eleana_par(dsc: dict, bruker_key: str) -> dict:
    value = dsc[bruker_key]
    value = value.split(' ')
    value_txt = value[0]
    value_txt = value_txt.replace("'", "")
    return value_txt
    #working_parameters[key] = value_txt
def dsc2eleana(key: str) -> str:
    ''' This function translates keys from Bruker to Eleana Parameter format'''
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
    try:
        bruker_key = dsc2eleana[key]
    except:
        bruker_key = ''
    return bruker_key

def par2eleana(key: str, format = 'emx') -> str:
    parEMX2eleana_single = {
                              'unit_x': 'JUN',
                              'name_x': 'JEX',
                              'unit_y': '',
                              'name_y': '',
                              'unit_z': '',
                              'name_z': 'JEY',
                              'MwFreq': 'MF',
                              'ModAmp': 'RMA',
                              'ModFreq': 'ModFreq',
                              'ConvTime': 'RCT',
                              'SweepTime': 'HSW',
                              'Tconst': 'RTC',
                              'Reson': 'RESO',
                              'Power': 'MP',
                              'PowAtten': 'MPD'
                              }

    parEMX2eleana_stack = {
                                    'unit_x': 'JUN',
                                    'name_x': 'JEX',
                                    'unit_y': '',
                                    'name_y': '',
                                    'unit_z': '',
                                    'name_z': 'JEY',
                                    'MwFreq': 'MF',
                                    'ModAmp': 'RMA',
                                    'ModFreq': 'ModFreq',
                                    'ConvTime': 'RCT',
                                    'SweepTime': 'HSW',
                                    'Tconst': 'RTC',
                                    'Reson': 'RESO',
                                    'Power': 'MP',
                                    'PowAtten': 'MPD'
                                 }

    parESP2eleana_single = {
                     'unit_x': 'XXUN',
                     'name_x': 'JEX',
                     'unit_y': 'XYUN',
                     'name_y': 'IRNAM',
                     'unit_z': '',
                     'name_z': 'JEY',
                     'MwFreq': 'MF',
                     'ModAmp': 'RMA',
                     'ConvTime': 'RCT',
                     'SweepTime': 'HSW',
                     'Tconst': 'RTC',
                     'Reson': 'RESO',
                     'Power': 'MP',
                     'PowAtten': 'MPD'
                     }
    if format == 'emx':
        try:
            bruker_key = parEMX2eleana_single[key]
        except:
            bruker_key = ''
        return bruker_key
    elif format == 'emx_stack':
        try:
            bruker_key = parEMX2eleana_stack[key]
        except:
            bruker_key = ''
        return bruker_key
    elif format == 'esp':
        try:
            bruker_key = parESP2eleana_single[key]
        except:
            bruker_key = ''
        return bruker_key

    else:
        try:
            bruker_key = parESP2eleana[key]
        except:
            bruker_key = ''
        return bruker_key