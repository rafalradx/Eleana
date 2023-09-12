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


# Classes of data objects

class Spectrum_CWEPR():
    par = {
        'groups': [],
        'name': '',
        'title': '',
        'type': '',
    }

    comments = Eleana.notes

    data_x = np.array([])
    data_y = np.array([])

if __name__ == "__main__":
    pass