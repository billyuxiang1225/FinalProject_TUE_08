import collections
from collections import OrderedDict
import boto3
import sys
import json
sys.path.insert(0,'../utils/')
import aws,time
from aws import *
from boto3.dynamodb.conditions import Key, Attr
import datetime
import base64
import os


getCredentials()
client_ml = getClient('machinelearning','us-east-1')

data_s3_url = "s3://ubisound/data100.csv"
train_percent = 80
name = 'ubisound100'
schema = '{"version" : "1.0","rowId" : null,"rowWeight" : null,"targetAttributeName" : "activity","dataFormat" : "CSV","dataFileContainsHeader" : true,"attributes" : [{"attributeName" : "band1","attributeType" : "NUMERIC"}, {"attributeName" : "band2","attributeType" : "NUMERIC"}, {"attributeName" : "energy","attributeType" : "NUMERIC"}, {"attributeName" : "zcr","attributeType" : "NUMERIC"}, {"attributeName" : "activity","attributeType": "CATEGORICAL"} ],"excludedAttributeNames" : [ ]}'
train_ds_id = 'ds-' + base64.b32encode(os.urandom(10))
test_ds_id = 'ds-' + base64.b32encode(os.urandom(10))


spec = {
	"DataLocationS3": data_s3_url,
        "DataRearrangement": json.dumps({
      	"splitting": {
     		"percentBegin": 0,
        	"percentEnd": train_percent
            }
        }),
        "DataSchema": schema
    	}


client_ml.create_data_source_from_s3(
        DataSourceId=train_ds_id,
        DataSpec=spec,
        DataSourceName=name + " - training split",
        ComputeStatistics=True
    	)


print("Created training data set %s" % train_ds_id)

spec['DataRearrangement'] = json.dumps({
    	"splitting": {
        	"percentBegin": train_percent,
            	"percentEnd": 100
        }
    	})

client_ml.create_data_source_from_s3(
        DataSourceId=test_ds_id,
       	DataSpec=spec,
        DataSourceName=name + " - testing split",
        ComputeStatistics=True
    	)

print("Created test data set %s" % test_ds_id)



