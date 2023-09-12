import numpy as np
from pathlib import Path, PurePath
import re
test_file = '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/cw.DSC'

class Elexsys():

    def create_single_CWEPR_spectrum(self, x_axis: list, dta: list, dsc: dict):
        pass

    def create_stacked_CWEPR_spectra(self, x_axis: list, dta: list, dsc: dict, ygf: list):
        pass

    def create_complex_EPR_data(self, x_axis: list, dta: list, dsc: dict):
        pass

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
                    ygf = np.fromfile(ygf_binary, dtype='>d')
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
                dsc[element[0].upper()] = element[1]
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

        # Collected data from Elexsys in x_axis, dta, ygf, dsc
        # Check if dta contains stack of spectra:




        if dsc['YTYP'] == 'NODATA' and dsc['EXPT'] == 'CW':
            self.create_single_CWEPR_spectrum(x_axis, dta, dsc)  # <-- This will create simple CW EPR spectrum

        elif dsc['YTYP'] != 'NODATA' and dsc['EXPT'] == 'CW':
            self.create_stacked_CWEPR_spectra()     # <-- This will create stacked CW EPR spectra




        # Tutaj skończyłem

        elif dsc['IKKF'] != 'REAL':
            self.create_complex_EPR_data()



    def dsc2par(self, dsc: dict):
        bruker2eleana = {'TITL'  : 'title',
                         'XUNI'  : 'unit-X',
                         'XNAM'  : 'name-X',
                         'YUNI'  : 'unit-Y',
                         'IRNAM' : 'name-Y',
                         'YUNI'  : 'unit-Z',
                         'YNAM'  : 'name-Z',
                         'IKKF'  : 'Compl',
                         'FrequencyMon':'MwFreq',
                         'ModAmp':'ModAmpl',
                         'Modfreq':'Modfreq',
                         'ConvTime':'ConvTime',
                         'SweepTime':'SweepTime',
                         'TimeConst':'T-Const',
                         'RESO':'ResModel',
                         'Power' : 'Power',
                         'PowerAtten':'Attenu'
                         }





if __name__ == "__main__":
    elexsys = Elexsys()
    wynik = elexsys.read(test_file)
