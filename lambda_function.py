import boto3
import io
import numpy as np
import pandas as pd
from io import StringIO # python3; python2: BytesIO 

def lambda_handler(event, context):
    bucket=''
    file_key=''
    
    runtime = boto3.Session().client('sagemaker-runtime')

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    mean_house = pd.read_csv(io.BytesIO(obj['Body'].read()),header=None)
    
    if 'Unnamed: 0' in mean_house.columns.tolist():
        mean_house.drop(['Unnamed: 0'], axis=1, inplace=True)
        
    user_vars = event['body']
    
    mean_house['HouseStyle'] = int(user_vars)
    mean_house = mean_house.astype('int32')
    
    ### change starts here
    test_file = io.StringIO()
    mean_house = mean_house.iloc[:,1:-1].astype('int32')
    mean_house.to_csv(test_file,header = None)

    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName= '',
        Body= test_file.getvalue(),
        ContentType = 'text/csv')
    #### change stops here
    
    result = response['Body'].read().decode('utf-8') 
    # result = str(result)[2:-1]
    result = round(float(result), 2)
   
    return {
        'statusCode' : 200,
            'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
            'body' : result
        }

