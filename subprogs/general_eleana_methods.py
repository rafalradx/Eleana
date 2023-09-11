import sys
from typing import List, Any

import numpy as np
from pathlib import Path
import tempfile

notes = {"content": "",
         "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [],
                  "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [], "text white": [],
                  "text grey": [], "text blue": [], "text green": [], "text red": []}}


class Eleana():
    # Set the most important directories for the program
    interpreter = sys.executable

    paths = {'program_dir': Path(__file__).resolve().parent,
             'home_dir': Path.home(),
             'tmp_dir': tempfile.gettempdir(),
             'pixmaps': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'ui': Path(Path(__file__).resolve().parent, "../pixmaps"),
             'subprogs': Path(Path(__file__).resolve().parent, ""),
             'last_import_dir': '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/'
             }

    # Create class for single spectrum
    class Spectrum():
        par = {
            'groups': [],
            'name': '',
            'title': '',
            'type': '',
        }

        comments = notes

        data_x = np.array([])
        data_y = np.array([])

    # ----- Methods definition of Eleana subprogs ------

    # Method for saving temporary text file in file /tmp
    def create_tmp_file(self, filename, content="Zawartość"):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        with open(path_to_file, "w") as file:
            file.write(content)

    # Method fo reading temporary text file in /tmp
    def read_tmp_file(self, filename):
        path_to_file = Path(Eleana.paths['tmp_dir'], filename)
        print('Read tmp_file: ', path_to_file)
        with open(path_to_file) as file:
            file_content = file.read()
        return file_content  #

    # Loading elexsys spectrum from a file
    def load_elexsys(self, filenames: tuple):
        elexsys_DTA_files = []
        elexsys_DSC_files = []
        elexsys_YGF_files = []

        for filename in filenames:
            filename = filename[:-3]

            # Prepare list of DTA, DSC and YGF files
            dta = filename + 'DTA'
            dsc = filename + 'DSC'
            ygf = filename + 'YGF'
            elexsys_DTA_files.append(dta)
            elexsys_DSC_files.append(dsc)
            elexsys_YGF_files.append(ygf)

        # Loading dta and dsc from the files
        # DTA data will be in Y_data
        # DSC data will be in desc_data
        # YGF (if exist) will be in ygf_data
        # errors list contain list of encountered error in loading DTA and/or DSC not YGF
        error = False
        try:
            # Load DTA and DSC
            y_data: list[Any] = []
            desc_data = []
            ygf_data = []

            # Loading DTA files from the elexsys_DTA_files list.
            for dta_binary in elexsys_DTA_files:
                if error == False:
                    try:
                        y = np.fromfile(dta_binary, dtype='>d')
                        y_data.append(y)
                    except:
                        error = True
                else:
                    break

            for dsc_file in elexsys_DSC_files:
                if error == False:
                    try:
                        with open(dsc_file, "r") as file:
                            dsc_content = file.read()
                            desc_data.append(dsc_content)
                    except:
                        error = True
                else:
                    break

            if error == True:
                return "Error"

            # Read YGF. If it does not exist put NaN to the list
            for ygf_binary in elexsys_YGF_files:
                file = Path(ygf_binary)
                if file.exists():
                    try:
                        ygf_content = np.fromfile(ygf_binary, dtype='>d')
                        ygf_data.append(ygf_content)
                    except:
                        error = True
                else:
                    ygf_data.append([np.NAN])

            # If there are not errors while reading DTA, DSC and YGF return
            if error == True:
                # If there are not errors while reading DTA, DSC and YGF return
                return {'status': False}, elexsys_DSC, elexsys_DTA, elexsys_YGF, bruker_YGF_exists
        # In case of error return only error
        except:
            y_data: list[Any] = []
            desc_data = []
            ygf_data = []
            return {'status': True, 'desc': traceback.format_exc()}

        # Tutaj będzie algorytm który analizuje co jest w plikach DSC i na tej podstawie generuje dalsze dane.
        ######################################################################################################

        for eachline in desc_data:
            lines = [line for line in eachline.splitlines() if line.strip()]
            i: str
            for i in lines:
                raw_par = i.split('\t')


        print(var)
        print(y_data)
        print(desc_data)
        print(ygf_data)
        print(var)