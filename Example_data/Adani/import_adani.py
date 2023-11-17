with open('adani.dat', 'rb') as file:
    content = file.read()
    adani = content.decode('utf-8', errors='ignore')

parameter = 'Center feld:'
multiply = 10
length = len(parameter)
cf_index = adani.find(f'asdadasdasddupa') + length
cf_end = adani.find('mT')
parameter_value = adani[cf_index:cf_end].strip()
try:
    parameter_value = float(parameter_value.replace(",", ".")) * multiply
except:
    parameter_value = -1
print(parameter_value)
