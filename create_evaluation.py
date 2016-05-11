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
    DataSourceId='ds-SENMWJDFYVHFRWGM',
    Verbose=True
)
print data_source['DataSourceId']

ml_model = client_ml.get_ml_model(
    MLModelId='ubisound_ml_100',
    Verbose=True
)


evaluation = client_ml.create_evaluation(
    EvaluationId='ubisound_ml_evaluation100',
    EvaluationName='ubisound_evaluation100',
    MLModelId=ml_model['MLModelId'],
    EvaluationDataSourceId=data_source['DataSourceId']
)

print evaluation['EvaluationId']

