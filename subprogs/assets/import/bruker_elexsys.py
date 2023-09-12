import numpy as np
test_file = '/home/marcin/PycharmProjects/Eleana/Example_data/Elexsys/cw.DSC'

def readElexsys(filename: str):
    elexsys_DTA = filename[:-3]+'DTA'
    elexsys_DSC = filename[:-3]+'DSC'
    elexsys_YGF = filename[:-3]+'YGF'

    # Loading dta and dsc from the files
    # DTA data will be in Y_data
    # DSC data will be in desc_data
    # YGF (if exist) will be in ygf_data
    # errors list contain list of encountered error in loading DTA and/or DSC not YGF

    error = False
    dta = []
    dsc_text = ''
    ygf = []

    try:
        # Load DTA from the elexsys_DTA
        dta = np.fromfile(dta_binary, dtype='>d')
    except:
        error = True
    else:
        return {"Error":True,'desc':f"Error in loading {elexsys_DTA}"}

    # If DTA sucessfully opened then read DSC
    if error != True:
        try:
            with open(elexsys_DSC, "r") as file:
                dsc_text = file.read()
        except:
            return {"Error": True, 'desc': f"Error in loading {elexsys_DSC}"}

        print(dsc)
        print(d)

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

    desc_table = [{}]
    # Read the DSC content
    for eachline in desc_data:
        lines = [line for line in eachline.splitlines() if line.strip()]
        i: str
        desc_single = {}

        for i in lines:
            raw_par = i.split('\t')
            try:
                par = raw_par[0]
                val = raw_par[1]
                desc_single[par] = val

            except:
                pass
        desc_table.append(desc_single)
    print(desc_table)

    # Create X axis
    error = False
    try:
        points = int(desc_data['XPTS'])
        x_min = float(desc_data['XMIN'])
        x_wid = float(desc_data['XWID'])
        step = x_wid / points
        x_axis = []
        for i in range(0, points):
            x_axis.append(i * step + x_min)
        x_data = np.array(x_axis)
    except:
        return {'status': True, 'desc': traceback.format_exc()}

    # Colected data from Elexsys
    print(x_data)
    print(y_data)
    print(desc_data)
    print(ygf_data)

    exit()
'''
if __name__ == "__main__":
    readElexsys(test_file)
