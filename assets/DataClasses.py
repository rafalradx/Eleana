from pathlib import Path
import numpy as np
from modules.ShimadzuSPC.shimadzu_spc import load_shimadzu_spc
from modules.Magnettech.magnettech import load_magnettech
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal

# how bruker Elexsys parameters are mapped to eleana parameters
# If you want eleana to extract more parameters from dsc
# just add them here
ELEANA_ELEXSYS_KEY_MAP = {
    'title': 'TITL',
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

ELEANA_ADANI_KEY_MAP = {
    "ModAmp": "mod_amplitude_G",        
    "PowAtten": "power_dB",  
    "ReceivGain": "gain",       
    "SweepTime": "sweep_time_s",        
    "ScansDone": "pass_number",       
}

ELEANA_EMX_SINGLE_MAP = {
    'unit_x': 'JUN',
    'MwFreq': 'MF',
    'ModAmp': 'RMA',
    'ConvTime': 'RCT',
    'SweepTime': 'HSW',
    'TimeConst': 'RTC',
    'Power': 'MP',
    'PowAtten': 'MPD'
    }

ELEANA_EMX_STACK_MAP = {
    'unit_x': 'XXUN',
    'MwFreq': 'MF',
    'ModAmp': 'RMA',
    'ConvTime': 'RCT',
    'SweepTime': 'HSW',
    'TimeConst': 'RTC',
    'Power': 'MP',
    'PowAtten': 'MPD'
    }

ELEANA_ESP_MAP = {
    'MwFreq': 'MF',
    'ModAmp': 'RMA',
    'ConvTime': 'RCT',
    'SweepTime': 'HSW',
    'TimeConst': 'RTC',
    'Power': 'MP',
    }

def extract_eleana_parameters(input_pars: Dict[str,str], mapped: Dict[str,str]) -> dict:
    result = {}
    for eleana_key, mapped_key in mapped.items():
        if mapped_key in input_pars:
            val = input_pars[mapped_key].split(' ')[0].replace("'", "")
            result[eleana_key] = val
    return result

@dataclass
class BaseDataModel:
    name: str
    x: np.ndarray
    y: np.ndarray
    z: Optional[np.ndarray] = None
    parameters: Dict[str, str] = field(default_factory=dict)
    complex: bool = False
    type: Literal['single 2D', 'stack 2D'] = 'single 2D'
    origin: Literal['@import', '@result'] = '@import'
    name_nr: str = ''
    groups: List[str] = field(default_factory=lambda: ['All'])
    comment: str = ''
    stk_names: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data):
        return BaseDataModel(*data)
    
    def is_stack(self) -> bool:
        return self.type == 'stack 2D'
    
    def is_single(self) -> bool:
        return self.type == 'single 2D'
    
    def unfolded_stack(self) -> List["BaseDataModel"]:
        if not self.is_stack():
            return []
        if self.stk_names is not None:
            unfolded_stack = []
            for n, row in enumerate(self.y):
                stk_name = self.stk_names[n]
                new_name = f"{self.name}'/'{stk_name}"
                new_data = BaseDataModel(
                    name=new_name,
                    x=self.x.copy(),
                    y=row.copy(),
                    parameters=self.parameters.copy(),
                    type='single 2D',
                    complex=self.complex,
                    groups=self.groups.copy(),
                )
                unfolded_stack.append(new_data)
            return unfolded_stack
        else:
            return []
        
    def remove_from_stack_by_index(self, index: int):
        if self.is_stack():
            self.y = np.delete(self.y, index, axis=0)
            self.z = np.delete(self.z, index, axis=0)
            del self.stk_names[index]
            # if only one trace left after removing
            # convert to single 2d
            if len(self.z) == 1:
                self.type = "single 2D"
                self.name = f"{self.name}_{self.stk_names[0]}"
                self.y = self.y.flatten()
                self.z = None
                self.stk_names = None


@dataclass
class SpectrumEPR(BaseDataModel):
    source: Optional[Literal['Bruker Elexsys','Bruker ESP', 'Bruker EMX', 'Adani', 'Magnettech']] = None
    exp_type: Literal['CWEPR','Pulse EPR','SR EPR'] = 'CWEPR'

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

        parameters = extract_eleana_parameters(dsc, ELEANA_ELEXSYS_KEY_MAP)
        
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
            exp_type=exp_type,
            source='Bruker Elexsys'
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
            exp_type=exp_type,
            type = data_type,
            source='Bruker Elexsys'
        )
    
    @classmethod
    def from_adani(cls, name: str, data: list[tuple], parameters: dict[str,str]):
        # unpack tuple into two lists 
        x_vals, y_vals = zip(*data)
        x = np.array(x_vals, dtype=float)
        y = np.array(y_vals, dtype=float)

        eleana_parameters={
        'unit_x': 'G',
        'name_x': 'Field',
        'unit_y': 'a.u.',
        'name_y': 'Intensity',
        'Compl': 'REAL',
        }

        extracted_parameters = extract_eleana_parameters(parameters, ELEANA_ADANI_KEY_MAP)
        eleana_parameters.update(extracted_parameters)

        return cls(
            name=name,
            x=x,
            y=y,
            parameters=eleana_parameters,
            source='Adani'
        )
    
    @classmethod
    def from_esp(cls, name: str, dta: np.ndarray, parameters: dict[str,str]):
        try:
            points = len(dta)
            x_min = float(parameters['GST'])
            x_wid = float(parameters['GSI'])
            x_axis = np.linspace(start=x_min, stop=x_min+x_wid,num=points)
        except ValueError:
            return {'Error': True, 'desc': f'Cannot create x axis for {name}'}
        
        eleana_parameters={
        'unit_x': 'G',
        'name_x': 'Field',
        'unit_y': 'a.u.',
        'name_y': 'Intensity',
        'Compl': 'REAL',
        }

        extracted_parameters = extract_eleana_parameters(parameters, ELEANA_ESP_MAP)
        eleana_parameters.update(extracted_parameters)

        return cls(
            name=name,
            x=x_axis,
            y=dta,
            parameters=eleana_parameters,
            source='Bruker EMX'
        )

    @classmethod
    def from_emx(cls, name: str, dta: np.ndarray, parameters: dict[str,str]):
        
        eleana_parameters={
        'name_x': 'Field',
        'unit_y': 'a.u.',
        'name_y': 'Intensity',
        'Compl': 'REAL',
        }

        if "SSY" in parameters:
            # stack of cw spectra
            x_points = int(parameters['SSX'])
            x_min = float(parameters['XXLB'])
            x_wid = float(parameters['XXWI'])
            x_axis = np.linspace(start=x_min, stop=x_min+x_wid,num=x_points)

            z_points = int(parameters['SSY'])
            z_min = float(parameters['XYLB'])
            z_wid = float(parameters['XYWI'])
            z_axis = np.linspace(start=z_min, stop=z_min+z_wid,num=z_points)

            extracted_parameters = extract_eleana_parameters(parameters, ELEANA_EMX_STACK_MAP)
            eleana_parameters.update(extracted_parameters)

            # reshape values into 2D array
            # each trace in row (YPTS, XPTS)
            values_2D = dta.reshape(z_points,x_points)

            name_z = parameters.get('name_z','')
            unit_z = parameters.get('unit_z','')

            # stack names
            stk_names = [f"{name_z}_{each}_{unit_z}" for each in z_axis]


            return cls(
                name=name,
                x=x_axis,
                y=values_2D,
                z=z_axis,
                parameters=eleana_parameters,
                stk_names=stk_names,
                type='stack 2D',
                source='Bruker EMX'
            )


        else:
            try:
                points = len(dta)
                x_min = float(parameters['GST'])
                x_wid = float(parameters['GSI'])
                x_axis = np.linspace(start=x_min, stop=x_min+x_wid,num=points)
            except ValueError:
                return {'Error': True, 'desc': f'Cannot create x axis for {name}'}

            extracted_parameters = extract_eleana_parameters(parameters, ELEANA_EMX_SINGLE_MAP)
            eleana_parameters.update(extracted_parameters)

            return cls(
                name=name,
                x=x_axis,
                y=dta,
                parameters=eleana_parameters,
                source='Bruker EMX'
            )

@dataclass
class SpectrumUVVIS(BaseDataModel):
    source: Literal['Shimadzu'] = 'Shimadzu'
        
def createFromElexsys(filename: str):
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
            "desc": f"Missing file: {elexsys_DTA.name}"
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
    except (FileNotFoundError, OSError, KeyError, ValueError) as e:
        return {'Error': True, 'desc': f'Cannot load {elexsys_DSC.name}: {e}'}
    
    # read YGF when exists
    if elexsys_YGF.exists():
        try:
            ygf = np.fromfile(elexsys_YGF, dtype='>d')
        except (FileNotFoundError, OSError, KeyError, ValueError) as e:
                return {"Error": True, 'desc': f"Cannot load {elexsys_YGF.name}: {e}" }
    else:
            ygf = None

    required_keys = ['EXPT', 'YTYP', 'IKKF']
    missing_keys = [key for key in required_keys if key not in dsc]

    if missing_keys:
        return {
            'Error': True,
            'desc': f"Cannot determine spectrum type. Missing required parameters in DSC file: {', '.join(missing_keys)}"
        }
    
    return SpectrumEPR.from_elexsys(filepath.stem, dta, dsc, ygf)

def createFromEMX(filename: str) -> object:
    filepath = Path(filename)
    emx_SPC = filepath.with_suffix('.spc')
    emx_PAR = filepath.with_suffix('.par')
    dsc = {}
    dta = []

    # load parameters file and determine format
    try:
        with open(emx_PAR, 'r', encoding='ascii', errors='ignore') as file:
            firstline = file.readline()
            remaining_lines = file.readlines()
    except (FileNotFoundError, OSError, KeyError, ValueError) as e:
        return {'Error': True, 'desc': f'Cannot load {emx_PAR}: {e}'}
    
    if firstline.startswith("DOS"):
        spectr_format = 'emx'
    else:
        spectr_format = 'esp'

    # Load SPC to dta varaiable
    try:
        if spectr_format == 'emx':
            dta = np.fromfile(emx_SPC, dtype=np.float32)
        else:
            dta = np.fromfile(emx_SPC, dtype='>i4')  # big-endian int32
    except (FileNotFoundError, OSError, ValueError) as e:
        return {'Error': True, 'desc': f'Cannot load {emx_SPC}: {e}'}

    # Convert Par to dictionary and store in dsc dictionary
    # values converted into floats when applicable
    for line in remaining_lines:
        splitted = line.split(None, 1)
        if len(splitted) == 0:
            continue

        if not splitted[0].isalpha():
            continue

        key = splitted[0]
        value = splitted[1].strip() if len(splitted) > 1 else ''

        # try:
        #     value = float(value)
        # except ValueError:
        #     pass
        dsc[key]=value# store back as a string

    # if the format is esp
    if spectr_format == 'esp':
        return SpectrumEPR.from_esp(filepath.name, dta, dsc)
    else:
        return SpectrumEPR.from_emx(filepath.name, dta, dsc)
    
def createFromShimadzuSPC(filename: str):
    name = Path(filename).name
    spectrum = load_shimadzu_spc(filename)
    if spectrum == None:
        return {'Error':True, 'desc':f'Error when loading Shimadzu {name} file'}
    parameters = {   'unit_x': 'nm',
                    'name_x': 'Wavelength',
                    'unit_y': 'OD',
                    'name_y': 'Absorbance',
                    'unit_z': ''
                }
    return SpectrumUVVIS(
        name=Path(filename).name,
        x=np.array(spectrum['x']),
        y=np.array(spectrum['y']),
        parameters=parameters
    )

def createFromMagnettech(filename, mscope=1, pool = -1, rescale = -1, shift = 0):
    name = Path(filename).name
    spectrum = load_magnettech(filename, mscope, pool, rescale, shift)
    if spectrum == None:
        return {'Error': True, 'desc':f'Error when loading Shimadzu {name} file'}
    parameters={
        'unit_x': 'G',
        'name_x': 'Field',
        'unit_y': 'a.u.',
        'name_y': 'Intensity',
        'Compl': 'REAL',
        'ModAmp': spectrum['parameters']['ModAmp'],
        'PowAtten': spectrum['parameters']['PowAtten'],
        'Power': spectrum['parameters']['Power'],
        'SweepTime': spectrum['parameters']['SweepTime'],
        }
    
    return SpectrumEPR(
        name=name,
        x=np.array(spectrum['x']),
        y=np.array(spectrum['y']),
        parameters=parameters,
        source='Magnettech'        
    )

def createFromAdaniDat(filename: str | Path):
    # parse Adani .dat file
    # Beware of windows encoding - cp1252
    filepath = Path(filename)
    parameters = {}
    data = []

    # check for utf-8 encoding
    # fallback to cp1252
    try:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filepath, encoding='cp1252') as f:
            lines = f.readlines()

    for line in lines:
        reading_data = False
        line = line.strip()

        if not line or line.startswith('='):
            continue

        # Start of data section
        if line[0].isdigit():
            reading_data = True

        if reading_data:
            parts = line.split()
            if len(parts) >= 3:
                x = float(parts[1].replace(',', '.'))
                y = float(parts[2].replace(',', '.'))
                data.append((x, y))
            continue

        if line.startswith("Center field:"):
            parameters["center_field_G"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])*10.0}"
            continue

        if line.startswith("Sweep width:"):
            parameters["sweep_width_G"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])*10.0}"
            continue

        if line.startswith("Mod. amplitude:"):
            parameters["mod_amplitude_G"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])/100.0}"
            continue

        if line.startswith("Power attenuation:"):
            parameters["power_dB"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])}"
            continue

        if line.startswith("Gain value:"):
            expr = line.split(":")[1].replace(',', '.').strip()
            parameters["gain"] = f"{eval(expr)}"
            continue

        if line.startswith("Sweep time:"):
            parameters["sweep_time_s"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])}"
            continue

        if line.startswith("Pass number:"):
            parameters["pass_number"] = f"{int(line.split(":")[1].strip())}"
            continue

        if line.startswith("g-factor:"):
            parameters["g_factor"] = f"{float(line.split(":")[1].replace(',', '.').strip())}"
            continue

        if line.startswith("Sample temperature:"):
            parameters["sample_temp_C"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])}"
            continue

        if line.startswith("Set Sample temperature:"):
            parameters["set_sample_temp_C"] = f"{float(line.split(":")[1].replace(',', '.').split()[0])}"
            continue

    return SpectrumEPR.from_adani(filepath.name, data, parameters)