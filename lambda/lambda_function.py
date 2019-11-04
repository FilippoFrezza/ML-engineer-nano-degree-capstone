import boto3
import io
import numpy as np
import pandas as pd
from io import StringIO # python3; python2: BytesIO 
import logging
import json


def lambda_handler(event, context):
    bucket='sagemaker-us-west-2-967949086162'
    file_key='housing/mean_house.csv'
    
    runtime = boto3.Session().client('sagemaker-runtime')

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    mean_house = pd.read_csv(io.BytesIO(obj['Body'].read()))
    
    if 'Unnamed: 0' in mean_house.columns.tolist():
        mean_house.drop(['Unnamed: 0'], axis=1, inplace=True)  
    
    #user_vars = event['body']
    user_input = json.loads(event['body'])

    mean_house['LotArea'] = int(user_input['lot_area'])
    mean_house['MiscVal'] = int(user_input['misc_value'])
    mean_house['2ndFlrSF'] = int(user_input['sec_floor_area'])
    mean_house['BsmtFinSF1'] = int(user_input['quality_finished_area'])
    mean_house['BsmtFinSF2'] = int(user_input['quality_unfinished_area'])
    mean_house['MasVnrArea'] = int(user_input['masonry_veneer_area'])
    mean_house['BsmtUnfSF'] = int(user_input['unfinished_basement'])
    mean_house['LowQualFinSF'] = int(user_input['low_quality_areas'])
    mean_house['PoolArea'] = int(user_input['pool_area'])
    mean_house['3SsnPorch'] = int(user_input['porch_area'])

    mean_house = mean_house.astype('int32')
    
    ### change starts here
    test_file = io.StringIO()
    #mean_house = mean_house.iloc[:,1:-1].astype('int32')
    mean_house = mean_house.astype('int32')
    mean_house.to_csv(test_file,header = None, index=False)

    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName= 'sagemaker-pytorch-2019-11-04-15-18-15-285',
        Body= test_file.getvalue(),
        ContentType = 'text/csv')
    #### change stops here
    
    #result = response['Body'].read().decode('utf-8')
    result = response['Body'].read()
    
    #result = str(result)[2:-1]

    result = round(float(result), 2)
   
    return {
        'statusCode' : 200,
            'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
            'body' : result
        }