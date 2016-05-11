import sys
import subprocess
import numpy
import wave
import time
import csv
from time import time
import collections
from collections import OrderedDict
import boto3
import json
sys.path.insert(0,'../utils/')
import aws
from aws import *
from boto3.dynamodb.conditions import Key, Attr



def sendMessage(message):
        try:
		if (message == 'knock'):
			message = 'Knock Knock'
		else:
			message = 'Door Closed'
        	client_sns.publish(TopicArn=TOPIC_ARN, Message = message)
        except Exception as e:
                print e
                pass

####################################
##	Print to File
####################################
filename = './current_data' + '.wav'
TOPIC_NAME = 'Demo_Topic'
getCredentials()
client_ml = getClient('machinelearning','us-east-1')
client_sns  = getClient('sns','us-east-1')
sns = client_sns.create_topic(Name=TOPIC_NAME)
TOPIC_ARN = sns['TopicArn']


activity = {'1': "nothing",'2': "knock",'3': "closedoor",}

while(1):
	record_args = ["arecord", "-d", "5", "-f", "dat", "-c", "1", "-D", "hw:2,0", filename]
	p = subprocess.call(record_args)
        #### Read WAV file ####
        fp = wave.open(filename, 'r')
        dstr = fp.readframes(240000)
        data = numpy.fromstring(dstr, numpy.int16)	
        #### FFT frequency Domain ####
        data_freq = numpy.absolute(numpy.fft.rfft(data))
        #### Energy ####
        energy = numpy.sum(numpy.square(data_freq[499:15000] ))
        if (energy >= 706000000000000):
		print "Predict?: Yes"
		#### frequency  ####
		band1 = numpy.sum(data_freq[1000:2000])
		band1 = round(band1)
		band2 = numpy.sum(data_freq[3500:4500])
		band2 = round(band2)
		#### zcr  ####
		data = numpy.sign(data)
		data[data == 0] = -1
		zcr = len(numpy.where(numpy.diff(data))[0])/240000.0
		#### Prediction ####
		real_time_prediction = client_ml.predict(
    			MLModelId='ubisound_ml_100',
    			Record={
                		'band1':  str(band1),
                		'band2':  str(band2),
                		'energy': str(energy),
               	 		'zcr': str(zcr)
    			}, 
       
			PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
		)
		i =  real_time_prediction['Prediction']['predictedLabel']
		predict_activity =  activity.get(i)
		print predict_activity
		sendMessage(predict_activity)		
	else: 
		print "Predict?: No"
