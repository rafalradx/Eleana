#!/usr/bin/env python3
#_-*- coding: UTF-8 -*-

'''
pyspe2dat, Extracts data from Magnettech binary files.
Copyright (C) 2011  Christian Rickert <rc.email@icloud.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

#
# Module imports
#
import argparse, fnmatch, math, os, struct, sys, time

#
# Variable definitions
#
version = "1.9" # 2015-04-24
subfolder = "pyspe2dat"

#
# Function declarations
#
def header(name="Gnomovision", version="69", year="2012", author="Christian Rickert <mail@crickert.de>"):
    """Prints the header for the GPL 2.0 license."""
    print(name + " version " + version + "," + os.linesep +\
         "Copyright (C) " + year + " " + author + 2*os.linesep +\
          name + " comes with ABSOLUTELY NO WARRANTY." + os.linesep +\
         "This is free software, and you are welcome" + os.linesep +\
         "to redistribute it under certain conditions;" + os.linesep +\
         "see 'gpl-2.0.txt' for details." + 2*os.linesep)

def files(root="/home/user/", pattern="*"):
    """Returns all files in root matching the pattern."""
    abspath = os.path.abspath(root)
    for fileobject in os.listdir(abspath):
        filename = os.path.join(abspath, fileobject)
        if os.path.isfile(filename) and fnmatch.fnmatchcase(fileobject, pattern):
            yield os.path.join(abspath, filename)

def readsourcefile(sourcename="name"):
	'Converts the content of a single source file into a list of values.'
	global timestamp
	sourcepath = os.path.join(subfolder, sourcename + ".spe")
	lastmodification = time.localtime(os.path.getmtime(sourcepath))
	timestamp = time.strftime('%Y-%m-%d_%H:%M:%S', lastmodification)
	print("FILE: " + sourcename + ".spe")
	sys.stdout.write("READING...")
	with open(sourcepath, 'rb') as sourcefile:
		global sourcedata
		if btype == 1: # former MiniScopeControl model
			wordtype = 'H' # unsigned integer
			wordsize = 2
		elif btype == 2: # recent MiniScopeControl model
			wordtype = 'h' # signed integer
			wordsize = 2
		sourcedata = []
		byte = 0
		try:
			while True:
				sourcefile.seek(byte) # move to binary block
				data = sourcefile.read(wordsize) # read binary block
				sourcedata.append(float(struct.unpack(wordtype, data)[0])) # convert binary block
				byte += wordsize # next binary block
		except (IndexError, struct.error):
			pass
		finally:
			sys.stdout.write("[OK]")

def writerawfile(rawname="name", skip=False):
	'Stores a list of values permanently into a raw file. Can be skipped.'
	rawpath = os.path.join(workingdirectory, rawname + ".raw")
	sys.stdout.write("\t" + "CACHING...")
	if not skip:
		with open(rawpath, 'w') as rawfile:
			index = 0
			for data in sourcedata:
				rawfile.write(str(sourcedata[index]) + "\n")
				index += 1
		sys.stdout.write("[OK]")
	else:
		sys.stdout.write("[->]")

def writetargetfile(targetname="name"):
	'Stores a list of X and Y values together with an informative header into a target file.'
	targetpath = os.path.join(workingdirectory, targetname + ".dat")
	sys.stdout.write("\t" + "WRITING...")

	parameters = {'unit_x': 'G',
                  'name_x': 'Field',
                  'unit_y': 'a.u.',
                  'name_y': 'Intensity',
                  'Compl': False,
                  'MwFreq': '',
                  'ModAmp': '',
                  'ModFreq': '',
                  'ConvTime': '',
                  'SweepTime': '',
                  'Tconst': '',
                  'Reson': '',
                  'Power': '',
                  'PowAtten': ''
                  }


	with open(targetpath, 'w') as targetfile:
		# Header
		# Parametric information is attached to the end of each sourcefile, hence accessing values with negative indices.
		# Each parameter is a floating point value with two decimal digits - but is stored as two consecutive integers.
		targetfile.write("{0:<2}{1:<1}".format("#\t", targetname) + "\n")
		targetfile.write("{0:<2}{1:<10}".format("#\t", timestamp) + "\n")
		centerfield = sourcedata[-32] + sourcedata[-31] / 100.0
		#targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Center_field_position:", centerfield, "G") + "\n")
		sweepwidth = sourcedata[-30] + sourcedata[-29] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Field_sweep_width:", sweepwidth, "G") + "\n")
		modulation = sourcedata[-28] + sourcedata[-27] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Field_modulation_amplitude:", modulation, "mG") + "\n")
		attenuation = sourcedata[-26] + sourcedata[-25] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Microwave_attenuation:", attenuation, "dB") + "\n")
		power = 10.0**((20.0-attenuation)/10.0)
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Microwave_power:", power, "mW") + "\n")
		sweeptime = sourcedata[-24] + sourcedata[-23] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Field_sweep_interval:", sweeptime, "s") + "\n")
		gainfactor = sourcedata[-22] + sourcedata[-21] / 100.0
		gainexponent = sourcedata[-20] + sourcedata[-19] / 100.0
		gain = gainfactor * 10**gainexponent
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Recording_gain:", gain, "[]") + "\n")
		averages = sourcedata[-18] + sourcedata[-17] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Number_of_scans_averaged:", averages, "[]") + "\n")
		phase = sourcedata[-16] + sourcedata[-15] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Phase_shift_setting:", phase, "°") + "\n")
		param1 = sourcedata[-14] + sourcedata[-13] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Undocumented_parameter_1:", param1, "[]") + "\n")
		param2 = sourcedata[-12] + sourcedata[-11] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Undocumented_parameter_2:", param2, "[]") + "\n")
		smoothing = sourcedata[-10] + sourcedata[-9] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Lowpass_filter_time:", smoothing, "s") + "\n")
		datapoints = sourcedata[-8] + sourcedata[-7] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Number_of_data_points:", datapoints, "[]") + "\n")
		param3 = sourcedata[-6] + sourcedata[-5] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Undocumented_parameter_3:", param3, "[]") + "\n")
		param4 = sourcedata[-4] + sourcedata[-3] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Undocumented_parameter_4:", param4, "[]") + "\n")
		param5 = sourcedata[-2] + sourcedata[-1] / 100.0
		targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Undocumented_parameter_5:", param5, "[]") + "\n")
		if amount == -1.0:
		 	poolsize = math.ceil(4096.0 / datapoints)
		else:
		 	poolsize = amount
		if poolsize != 1.0:
			targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Manual_datapoint_pool:", poolsize, "[]") + "\n")
		gaindivisor = (gain if divisor == -1 else divisor)
		if divisor != 1.0:
			targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Manual_rescaling_divisor:", gaindivisor, "[]") + "\n")
		if offset != 0.0:
			targetfile.write("{0:_<30}{1:_>9.2f}{2:_>3}".format("# Manual_baseline_shift:", offset, "[]") + "\n")
		#Body
		# X and Y values with column labels for Origin -
		# if necessary, averaging of values is performed here
		stepwidth = sweepwidth / 4096.0
		currentfield = centerfield - (sweepwidth / 2)
		poolsignal = 0.0
		poolcount = 1.0

		modulation_ampl = modulation / 10000
		parameters = {'unit_x': 'G',
					  'name_x': 'Field',
					  'unit_y': 'a.u.',
					  'name_y': 'Intensity',
					  'Compl': False,
					  'MwFreq': '',
					  'ModAmp': str(modulation_ampl),
					  'ModFreq': '',
					  'ConvTime': '',
					  'SweepTime': '',
					  'Tconst': '',
					  'Reson': '',
					  'Power': '',
					  'PowAtten': ''
					  }

		#targetfile.write("#Magnetic_Field\tEpr_Signal\n")


		''' TUTAJ SĄ ZAPISYWANE DANE '''


		amplitude = []
		field = []
		for currentsignal in sourcedata[:-32]:
			poolsignal += (currentsignal + offset) / gaindivisor
			if poolsize == 1.0:
				targetfile.write("{0:-.6f}\t{1:+.6f}".format(currentfield, poolsignal) + "\n")


				amplitude.append(poolsignal)
				field.append(currentfield)


				poolsignal = 0.0
				poolcount = 0.0
			elif poolcount == 1.0:
				startfield = currentfield
			elif poolcount % poolsize == 0.0:
				poolfield = startfield + (currentfield - startfield) / 2.0
				poolsignal /= poolsize
				targetfile.write("{0:-.6f}\t{1:+.6f}".format(poolfield, poolsignal) + "\n")
				poolsignal = 0.0
				poolcount = 0.0
			currentfield += stepwidth
			poolcount += 1.0
		print("[OK]." + os.linesep)

		return {'parameters':parameters, 'x':field, 'y':amplitude}
#
# Main program
#

# Parameters
parser = argparse.ArgumentParser(
	prog='pyspe2dat',
	description='Extracts data from Magnettech binary files.',
	epilog='Published under the terms of the GNU General Public License 2.0 (GPLv2):\
			http://www.gnu.org/licenses/gpl-2.0.html')
parser.add_argument('--mscope',
					help='choose MiniScopeControl model (DEFAULT: 1)',
					action='store',
					dest='btype',
					default=1.0)
parser.add_argument('--pool',
					help='manually pool datapoints (DEFAULT: -1.0)',
					action='store',
					dest='amount',
					default=-1.0)
parser.add_argument('--rescale',
					help='manually correct gain (DEFAULT: -1.0)',
					action='store',
					dest='divisor',
					default=-1.0)
parser.add_argument('--shift',
					help='manually correct offset (DEFAULT: -16384.0)',
					action='store',
					dest='offset',
					default=-16384.0)
parser.add_argument('-v', '--version',
					help='show version number and exit',
					action='version',
					version='%(prog)s ' + version)
args = parser.parse_args()
btype = int(args.btype)
amount = (-1.0 if float(args.amount) == -1.0 else math.ceil(abs(float(args.amount))))
divisor = (1.0 if float(args.divisor) <= 0.0 and float(args.divisor) != -1.0 else float(args.divisor))
offset = float(args.offset)

# Copyright
header(name="pyspe2dat", version=version, year="2011", author="Christian Rickert <mail@crickert.de>")

try:
	# Mainpart
	#print("DIRECTORY: " + subfolder + 2*os.linesep)
	workingdirectory = os.path.abspath(subfolder)
	if not os.path.exists(workingdirectory):
		os.mkdir(workingdirectory)
	filecount = 0
	start = time.time()
	for sourcefile in files(root=subfolder, pattern="*.spe"):
		name = os.path.splitext(os.path.split(sourcefile)[1])[0]
		readsourcefile(name)
		writerawfile(name, skip=True)
		spectrum = writetargetfile(name)

		print(spectrum)
except:
	print('Error')

	# 	filecount += 1
	# end = time.time()
	# duration = end - start

	# Summary
# 	summary = "Total of " + str(filecount) + str(" files " if filecount != 1 else " file ") + "processed in " +\
# 			   str("{0: <5.3f}".format(duration)) + str(" seconds." if duration != 1 else " second.")
# 	decorator = "{0:=^" + str(len(summary)) + "}"
# 	print(decorator.format(""))
# 	print(decorator.format(summary))
# 	print(decorator.format("") + os.linesep * 2)
# 	#time.sleep(5)
# except KeyboardInterrupt:
#     print(os.linesep * 2 + "Program stopped by user." + os.linesep * 2)
# finally:
# 	pass