import numpy
import wave
import time
import csv

start = time.time()
### save to csv ###
fieldnames = ['band1', 'band2', 'energy', 'zcr', 'activity']
behavior = ['nothing', 'knock','closedoor']
energy_avg = [0, 0, 0, 0]
with open('data_100.csv','w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
	for bh in behavior:
		for i in range(1,101):	
			#### Read WAV file ####
			wavefile = './data/' + bh + str(i) + '.wav'
			fp = wave.open(wavefile, 'r')
			dstr = fp.readframes(240000)
			data = numpy.fromstring(dstr, numpy.int16)
			#### FFT frequency Domain ####
			data_freq = numpy.absolute(numpy.fft.rfft(data))
			#### frequency  ####
			band1 = numpy.sum(data_freq[1000:2000])
			band1 = round(band1)
			#print 'band1:' + str(band1)
			band2 = numpy.sum(data_freq[3500:4500])
			band2 = round(band2)
			#print 'band2:' + str(band2)
			#### Energy ####
			#print len(data_freq[499:15000])
			energy = numpy.sum(numpy.square(data_freq[499:15000] )) # 80~14000 Hz
			#print 'Energy:' + str(energy)
			#### zcr  ####
			data = numpy.sign(data)
			data[data == 0] = -1 
			zcr = len(numpy.where(numpy.diff(data))[0])/240000.0
			#print 'zcr:' + str(zcr)

			#### Print Time Takes ####
			#end = time.time()
			#print 'Time Escape:' + str(end - start) + ' s'
			cs = 0;
			if bh == 'nothing':
				cs = 1;
			elif bh == 'knock':
				cs = 2;
			elif bh == 'closedoor':
				cs = 3;
			energy_avg[cs-1] = energy_avg[cs] + energy	
			writer.writerow({'band1':band1, 'band2':band2, 'energy':energy, 'zcr': zcr, 'activity':cs})
print 'nothing:' + str(energy_avg[0]/100)
print 'knock' + str(energy_avg[1]/100)
print 'closedoor' + str(energy_avg[2]/100)

