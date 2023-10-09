import numpy as np
from pathlib import Path, PurePath
import re
from assets.general_eleana_methods import *



class Elexsys():
    def read(self, filename: str) -> object:
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



if __name__ == "__main__":
    elexsys = Elexsys()
    elexsys.read(test_file)