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

getCredentials()
client_ml = getClient('machinelearning','us-east-1')


data_source = client_ml.get_data_source(
    DataSourceId='ds-CUKHCG4U6UDBHXOK',
    Verbose=True
)
print data_source['DataSourceId']


ml_model = client_ml.create_ml_model(
    MLModelId='ubisound_ml_100',
    MLModelName='ubisound_ml_model_100',
    MLModelType='MULTICLASS',
    TrainingDataSourceId=data_source['DataSourceId'],
)
print ml_model['MLModelId']

