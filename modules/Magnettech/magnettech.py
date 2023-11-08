import math, struct
from pathlib import Path


''' Parametry z argparse '''

def load_magnettech(filename, mscope=1, pool = -1, rescale = -1, shift = 0):
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

	The original pyspe2dat 1.9 2015-04-24 was modified to fit Eleana program

	Parameters for function:

	mscope = 1 # Starszy model MiniScope
	mscope = 2 # Nowszy model
	pool = -1 # Wartości o 1 do 8. -1 to brak
	rescale = -1
	shift = 0
	'''

	btype = int(mscope)
	amount = (-1.0 if float(pool) == -1.0 else math.ceil(abs(float(pool))))
	divisor = (1.0 if float(rescale) <= 0.0 and float(rescale) != -1.0 else float(rescale))
	offset = float(shift)

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

	name = Path(filename).name
	try:
		with open(filename, 'rb') as sourcefile:
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

		centerfield = sourcedata[-32] + sourcedata[-31] / 100.0
		sweepwidth = sourcedata[-30] + sourcedata[-29] / 100.0
		modulation = sourcedata[-28] + sourcedata[-27] / 100.0
		modulation = modulation / 1000
		parameters['ModAmp'] = modulation
		attenuation = sourcedata[-26] + sourcedata[-25] / 100.0
		parameters['PowAtten'] = attenuation
		power = 10.0 ** ((20.0 - attenuation) / 10.0)
		parameters['Power'] = power
		sweeptime = sourcedata[-24] + sourcedata[-23] / 100.0
		parameters['SweepTime'] = sweeptime
		gainfactor = sourcedata[-22] + sourcedata[-21] / 100.0
		gainexponent = sourcedata[-20] + sourcedata[-19] / 100.0
		gain = gainfactor * 10 ** gainexponent
		averages = sourcedata[-18] + sourcedata[-17] / 100.0
		phase = sourcedata[-16] + sourcedata[-15] / 100.0
		param1 = sourcedata[-14] + sourcedata[-13] / 100.0
		param2 = sourcedata[-12] + sourcedata[-11] / 100.0
		smoothing = sourcedata[-10] + sourcedata[-9] / 100.0
		datapoints = sourcedata[-8] + sourcedata[-7] / 100.0
		param3 = sourcedata[-6] + sourcedata[-5] / 100.0
		param4 = sourcedata[-4] + sourcedata[-3] / 100.0
		param5 = sourcedata[-2] + sourcedata[-1] / 100.0
		if amount == -1.0:
			poolsize = math.ceil(4096.0 / datapoints)
		else:
			poolsize = amount
		gaindivisor = (gain if divisor == -1 else divisor)

		# X and Y values with column labels for Origin -
		# if necessary, averaging of values is performed here
		stepwidth = sweepwidth / 4096.0
		currentfield = centerfield - (sweepwidth / 2)
		poolsignal = 0.0
		poolcount = 1.0

		amplitude = []
		field = []
		for currentsignal in sourcedata[:-32]:
			poolsignal += (currentsignal + offset) / gaindivisor
			if poolsize == 1.0:
				amplitude.append(poolsignal)
				field.append(currentfield)
				poolsignal = 0.0
				poolcount = 0.0
			elif poolcount == 1.0:
				startfield = currentfield
			elif poolcount % poolsize == 0.0:
				#	poolfield = startfield + (currentfield - startfield) / 2.0
				poolsignal /= poolsize
				poolsignal = 0.0
				poolcount = 0.0
			currentfield += stepwidth
			poolcount += 1.0

		return {'parameters': parameters, 'x': field, 'y': amplitude}
	except:
		return None
