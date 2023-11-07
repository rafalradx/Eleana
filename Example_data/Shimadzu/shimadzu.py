from pyspc import spc

# Wczytaj plik SPC
spc_file = spc.SpcFile("widmo.spc")

# Pobierz dane spektroskopowe
wavelengths = spc_file.data.xdata
intensities = spc_file.data.ydata

print(wavelengths)