import collections
from collections import OrderedDict
import boto3
import sys
import json
sys.path.insert(0,'../utils/')
import aws,time
from aws import *
from boto3.dynamodb.conditions import Key, Attr
import numpy
import wave
import time
import csv

getCredentials()
client_ml = getClient('machinelearning','us-east-1')
activity = {'1': "nothing",'2': "knock",'3': "closedoor",}

start = time.time()
#### Read WAV file ####
wavefile = './knock_test' + '.wav'
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
energy = numpy.sum(numpy.square(data_freq[499:15000] )) # 80~14000 Hz
#print 'Energy:' + str(energy)
#### zcr  ####
data = numpy.sign(data)
data[data == 0] = -1 
zcr = len(numpy.where(numpy.diff(data))[0])/240000.0
#print 'zcr:' + str(zcr)

#### Print Time Takes ####
end = time.time()
print 'Time Calculate: ' + str(end - start) + ' s'


#### Prediction ####
real_time_prediction = client_ml.predict(
    MLModelId='ubisound_ml',
    Record={
    		'band1':  str(band1),
		'band2':  str(band2),
		'energy': str(energy),
		'zcr': str(zcr)        
    },
    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
)

type =  real_time_prediction['Prediction']['predictedLabel']



#### Print Time Takes ####
end = time.time()
print 'Time Escape: ' + str(end - start) + ' s'


print activity.get(type)
