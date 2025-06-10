from pathlib import Path
import numpy as np
import re
from modules.ShimadzuSPC.shimadzu_spc import load_shimadzu_spc
from modules.Magnettech.magnettech import load_magnettech
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal

# how bruker parameters are mapped to eleana parameters
ELEANA_TO_BRUKER_KEY_MAP = {'title': 'TITL',
            'unit_x': 'XUNI',
            'name_x': 'XNAM',
            'unit_y': 'IRUNI',
            'name_y': 'IRNAM',
            'unit_z': 'YUNI',
            'name_z': 'YNAM',
            'Compl': 'IKKF',
            'MwFreq': 'FrequencyMon',
            'ModAmp': 'ModAmp',
            'ModFreq': 'ModFreq',
            'ConvTime': 'ConvTime',
            'SweepTime': 'SweepTime',
            'TimeConst': 'TimeConst',
            'Reson': 'RESO',
            'Power': 'Power',
            'PowAtten': 'PowerAtten',
            'Harmonic': 'Harmonic',
            'B_zero': 'B0VL',
            'ShotRepTime': 'ShotRepTime'
            }

def extract_eleana_parameters(dsc: dict) -> dict:
    result = {}
    for eleana_key, bruker_key in ELEANA_TO_BRUKER_KEY_MAP.items():
        if bruker_key in dsc:
            #print(f"{bruker_key}: {dsc[bruker_key]}")
            val = dsc[bruker_key].split(' ')[0].replace("'", "")
            result[eleana_key] = val
    return result

class Single2D:
    def __init__(self, data: dict):
        self.parameters: dict = data['parameters']
        self.groups: list = data['groups']
        self.x: np.ndarray = np.array(data['x'])
        self.y: np.ndarray = np.array(data['y'])
        self.z = None
        self.name: str = data['name']
        self.complex = data.get('complex', False)
        self.type = 'single 2D'
        self.origin = data.get('origin', '')
        self.name_nr = ''
        self.comment = data.get('comment', '')

class Stack:
    def __init__(self, data: dict):
        self.parameters: dict = data['parameters']
        self.groups: list = data['groups']
        self.x: np.ndarray = np.array(data['x'])
        self.y: np.ndarray = np.array(data['y'])
        self.name: str = data['name']
        self.complex = data.get('complex', False)
        self.type = 'stack 2D'
        self.origin = data.get('origin', '')
        self.name_nr = ''
        self.comment = data.get('comment', '')
        self.stk_names = data['stk_names']
        z_axis = data.get('z', None)
        if not z_axis:
            self.z = None
        else:
            self.z = np.array(z_axis)

class Spectrum_CWEPR:
    def __init__(self, name: str, x_axis: np.ndarray, dta: np.ndarray, dsc: dict, format="elexsys"):
        self.parameters = {'title': '', 'unit_x': 'G', 'name_x': 'Field', 'name_y': 'Intensity', 'MwFreq': '', 'ModAmp': '', 'ModFreq': '',
                           'ConvTime': '',  'SweepTime': '',  'TimeConst': '',  'Reson': '',  'Power': '', 'PowAtten': ''}
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

        if format =="elexsys":
            working_par = extract_eleana_parameters(dsc)
        elif format in ('emx', 'esp'):
            for key in fill_missing_keys:
                try:
                    working_par[key] = create_eleana_par(dsc, par2eleana(key, format))
                except:
                    pass

        self.parameters = working_par
        self.x = np.array(x_axis)
        self.y = np.array(dta)
        self.z = None
        self.comment = ''

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
        z_axis = []
        # Create in stack names:
        for each in ygf:
            name = working_parameters.get('name_z', '') + ' ' + str(each) + ' ' + working_parameters.get('unit_z', '')
            working_stk_names.append(name)
            z_axis.append(each)
        self.z = np.array(z_axis)
        self.stk_names = working_stk_names
        self.y = list_of_y_array
        self.type = 'stack 2D'
        self.complex = False
        self.origin = 'CWEPR'
        self.parameters = working_parameters
        self.comment = ''

@dataclass
class SpectrumEPR:
    name: str
    x: np.ndarray
    y: np.ndarray
    z: Optional[np.ndarray] = None
    parameters: Dict[str, str] = field(default_factory=dict)
    complex: bool = False
    type: Literal['single 2D', 'stack 2D'] = 'single 2D'
    origin: Literal['CWEPR', 'Pulse EPR'] = 'CWEPR'
    name_nr: str = ''
    groups: List[str] = field(default_factory=lambda: ['All'])
    comment: str = ''
    stk_names: Optional[List[str]] = None

    @classmethod
    def from_elexsys(cls, name: str, dta: np.ndarray, dsc: dict, ygf: Optional[np.ndarray] = None):

        # create x axis
        x_points = int(dsc['XPTS'])
        x_min = float(dsc['XMIN'])
        x_wid = float(dsc['XWID'])

        if x_points < 2:
            raise ValueError("XPTS must be at least 2")

        x_max = x_min + x_wid
        # linspace creates points from x_min to x_max inclusive
        x_axis = np.linspace(x_min, x_max, x_points)

        parameters = extract_eleana_parameters(dsc)
        
        # DSC typically does not specify unit for intensity (empty IRUNI, IIUNI fields)
        # assign a.u.
        if parameters.get("unit_y") == '':
            parameters["unit_y"] = "a.u."
        
        if dsc['IKKF'] == 'CPLX':
            cplx = True
            # Convert interleaved real/imag to complex array
            values = np.array([complex(dta[i], dta[i+1]) for i in range(0, len(dta), 2)])
        else:
            cplx = False
            values = dta
        
        if dsc['EXPT'] == 'CW':
            exp_type = 'CWEPR'
        else:
            exp_type = 'Pulse EPR'

        # check for single 2D spectrum (not stack)
        if len(x_axis) == len(values):
            return cls(
            name=name,
            x=np.array(x_axis),
            y=values,
            parameters=parameters,
            complex=cplx,
            origin=exp_type
        )

        # if the size does not match, it means we have second dimention (stack spectrum)
        # change data type
        data_type = 'stack 2D'

        # create y axis
        # read second axis from ygf file if present
        if ygf is not None:
            y_axis = ygf
            y_points = len(ygf)
        else:
            # if not present, create second axis from parameters in dsc
            try:
                y_points = int(dsc['YPTS'])
                y_min = float(dsc['YMIN'])
                y_wid = float(dsc['YWID'])

                if y_points < 2:
                    raise ValueError("YPTS must be at least 2")

                y_max = y_min + y_wid
                # linspace creates points from x_min to x_max inclusive
                y_axis = np.linspace(y_min, y_max, y_points)
            except (KeyError, ValueError) as e:
                return {'Error': True, 'desc': f'Cannot create Y axis for {name}: {e}'}
        
        # reshape values into 2D array
        # each trace in row (YPTS, XPTS)
        values_2D = values.reshape(y_points,x_points)

        name_z = parameters.get('name_z','')
        unit_z = parameters.get('unit_z','')

        # stack names
        stk_names = [f"{name_z}_{each}_{unit_z}" for each in y_axis]

        return cls(
            name=name,
            x=np.array(x_axis),
            y=values_2D,
            z=y_axis, # it has to be that way
            parameters=parameters,
            stk_names=stk_names,
            complex=cplx,
            origin=exp_type,
            type = data_type
        )
        
def createFromElexsys(filename: str) -> object:
    # Loading dta and dsc from the files
    # DTA data will be in Y_data
    # DSC data will be in desc_data
    # YGF (if exist) will be in ygf_data
    # errors list contain list of encountered error in loading DTA and/or DSC not YGF

    filepath = Path(filename)
    ext = filepath.suffix  # extract extension .dsc .dta. ygf

    # Determine if extension is uppercase or lowercase
    if ext.isupper():
        ext_case = 'upper'
    elif ext.islower():
        ext_case = 'lower'
    else:
        ext_case = 'mixed'

    # Pick suffix format based on the input extension
    if ext_case == 'upper':
        dta_ext = '.DTA'
        dsc_ext = '.DSC'
        ygf_ext = '.YGF'
    elif ext_case == 'lower':
        dta_ext = '.dta'
        dsc_ext = '.dsc'
        ygf_ext = '.ygf'
    else:
        # Fallback: default to lowercase
        dta_ext = '.dta'
        dsc_ext = '.dsc'
        ygf_ext = '.ygf'

    # create path to files
    elexsys_DTA = filepath.with_suffix(dta_ext)
    elexsys_DSC = filepath.with_suffix(dsc_ext)
    elexsys_YGF = filepath.with_suffix(ygf_ext)

    # Check whether .DTA nad .DSC files exist
    if not elexsys_DSC.exists():
        return {
            "Error": True,
            "desc": f"Missing file: {elexsys_DSC.name}"
        }
    
    if not elexsys_DTA.exists():
        return {
            "Error": True,
            "desc": f"Missing file: {elexsys_DSC.name}"
        }

    # Load DTA from the elexsys_DTA
    try:
        dta = np.fromfile(elexsys_DTA, dtype='>d')
    except Exception as e:
        return {"Error": True, 'desc': f"Error in loading {elexsys_DTA.name}: {e}"}
    
    # If DTA sucessfully opened then read DSC and extract parameters into dictionary
    dsc = {}
    try:
        with open(elexsys_DSC, "r") as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('*') or line.startswith('#'):
                    continue

                # Split line into key and value
                if '\t' in line:
                    key, value = line.split('\t', 1)
                elif ' ' in line:
                    key, value = line.split(None, 1)  # split on first group of whitespace
                else:
                    key, value = line, ''

                dsc[key.strip()] = value.strip()
    except Exception as e:
        return {"Error": True, 'desc': f"Error in loading {elexsys_DSC.name}: {e}"}
    
    # read YGF when exists
    if elexsys_YGF.exists():
        try:
            ygf = np.fromfile(elexsys_YGF, dtype='>d')
        except:
                return {"Error": True, 'desc': f"Error in loading {elexsys_YGF.name}" }
    else:
            ygf = None

    # # create xaxis
    # try:
    #     points = int(dsc['XPTS'])
    #     x_min = float(dsc['XMIN'])
    #     x_wid = float(dsc['XWID'])
        
    #     if points < 2:
    #         raise ValueError("XPTS must be at least 2")

    #     x_max = x_min + x_wid
    #     # linspace creates `points` points from x_min to x_max inclusive
    #     x_axis = np.linspace(x_min, x_max, points)

    # except (KeyError, ValueError) as e:
    #     return {'Error': True, 'desc': f'Cannot create X axis for {elexsys_DTA}: {e}'}
    
    # Check if specific key are present in DSC
    # This keys are required for determination of spectrum type
    required_keys = ['EXPT', 'YTYP', 'IKKF']
    missing_keys = [key for key in required_keys if key not in dsc]

    if missing_keys:
        return {
            'Error': True,
            'desc': f"Cannot determine spectrum type. Missing required parameters in DSC file: {', '.join(missing_keys)}"
        }
    
    return SpectrumEPR.from_elexsys(filepath.stem, dta, dsc, ygf)

    # # Now create object containing particular type of data
    # # Process based on experiment type and data format
    # if dsc['EXPT'] == 'CW':
    #     if dsc['YTYP'] == 'NODATA':
    #         # Single CW EPR spectrum (no Y-dimension)
    #         #return Spectrum_CWEPR(filepath.stem, x_axis, dta, dsc)
    #         return SpectrumEPR.from_elexsys(filepath.stem, dta, dsc, ygf)
    #     else:
    #         # Stacked CW spectra (Y-dimension present)
    #         # chech again if ygf was loaded
    #         if ygf is None:
    #             return {
    #                 'Error': True,
    #                 'desc': f"The required .YGF file for stack CW spectrum is missing."
    #             }
            
    #         return SpectrumEPR.from_elexsys(filepath.stem, dta, dsc, ygf)

    #         # cw_stack = Spectra_CWEPR_stack(filepath.stem, x_axis, dta, dsc, ygf)

    #         # # I don't know what's going on here
    #         # # Consult MS
    #         # unit = cw_stack.parameters.get('unit_y', 'a.u.')
    #         # if unit == 's':
    #         #     cw_stack.parameters['unit_y'] = 'a.u.'

    #         # return cw_stack

    # elif dsc['IKKF'] == 'CPLX':
    #     # Complex-valued spectrum (e.g., pulsed EPR)
    #     return SpectrumEPR.from_elexsys(filepath.stem, dta, dsc, ygf)

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
             'groups':['All'],
             'x': np.array(spectrum['x']),
             'y': np.array(spectrum['y']),
             'name': name,
             'complex': False,
             'type': 'single2D',
             'origin': 'UV VIS spectrum'
             }
    spectrum = Single2D(data)
    return spectrum

def createFromMagnettech(filename, mscope=1, pool = -1, rescale = -1, shift = 0):
    spectrum = load_magnettech(filename, mscope, pool, rescale, shift)
    if spectrum == None:
        return {'Error': True, 'desc': 'Error'}
    par = spectrum['parameters']
    name = Path(filename).name
    data = {'parameters':
                {'unit_x': 'G',
                 'name_x': 'Field',
                 'unit_y': 'a.u.',
                 'name_y': 'Intensity',
                 'Compl': False,
                 'unit_z': '',
                 'ModAmp': par['ModAmp'],
                 'PowAtten': par['PowAtten'],
                 'Power': par['Power'],
                 'SweepTime': par['SweepTime'],
                  },
           'groups': ['All'],
           'x': np.array(spectrum['x']),
           'y': np.array(spectrum['y']),
           'name': name,
           'complex': False,
           'type': 'single2D',
           'origin': 'Magnettech EPR'
            }
    spectrum = Single2D(data)
    return spectrum

def createFromAdaniDat(filename, adani: dict):
    def _get_parameter(start: str, end: str, multiply: float):
        length = len(start)
        cf_index = adani.find(start) + length
        cf_end = adani.find(end)
        parameter_value = adani[cf_index:cf_end].strip()
        try:
            parameter_value = float(parameter_value.replace(",", ".")) * multiply
        except:
            parameter_value = -1
        return parameter_value
    adani = adani.strip()
    adani = adani.replace(',', '.')
    adani_lines = adani.splitlines()
    stripped_lines = []
    for line in adani_lines:
        line = line.strip()
        stripped_lines.append(line + '\n')
    adani = ''.join(stripped_lines[1:])
    adani_split = adani.split('==\n0')
    numbers = '0' + adani_split[1]
    rows = numbers.split('\n')
    columns = [row.split() for row in rows]
    x = []
    y = []
    for column in columns:
        try:
            field = float(column[1])*10
            amplitude = float(column[2])
            x.append(field)
            y.append(amplitude)
        except:
            pass
    data = {}
    data['parameters'] = {}
    data['parameters']['SweepTime'] = _get_parameter('Sweep time:', ' s\n', 1)
    data['parameters']['PowAtten'] = _get_parameter('Power attenuation:', ' dB\n', 1)
    data['parameters']['ModAmp'] = _get_parameter('Mod. amplitude:', ' uT\n', 0.01)
    data['parameters']['name_x'] = 'Field'
    data['parameters']['unit_x'] = 'G'
    data['x'], data['y'] = x, y
    data['name'] = filename.name
    data['groups'] = ['All']
    data['origin'] = 'Adani ESR'
    spectrum = Single2D(data)
    return spectrum


def create_eleana_par(dsc: dict, bruker_key: str) -> dict:
    value = dsc[bruker_key]
    value = value.split(' ')
    value_txt = value[0]
    value_txt = value_txt.replace("'", "")
    return value_txt

def dsc2eleana(key: str) -> str:
    ''' This function translates keys from Bruker to Eleana Parameter format'''
    dsc2eleana = {'title': 'TITL',
                  'unit_x': 'XUNI',
                  'name_x': 'XNAM',
                  'unit_y': 'IRUNI',
                  'name_y': 'IRNAM',
                  'unit_z': 'YUNI',
                  'name_z': 'YNAM',
                  'Compl': 'IKKF',
                  'MwFreq': 'FrequencyMon',
                  'ModAmp': 'ModAmp',
                  'ModFreq': 'ModFreq',
                  'ConvTime': 'ConvTime',
                  'SweepTime': 'SweepTime',
                  'TimeConst': 'TimeConst',
                  'Reson': 'RESO',
                  'Power': 'Power',
                  'PowAtten': 'PowerAtten',
                  'Harmonic': 'Harmonic',
                  'B_zero': 'B0VL',
                  'ShotRepTime': 'ShotRepTime'
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
                              'TimeConst': 'RTC',
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
                                    'TimeConst': 'RTC',
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
                     'TimeConst': 'RTC',
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