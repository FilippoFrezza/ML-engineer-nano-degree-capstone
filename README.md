# ML-engineer-nano-degree-capstone

Deployment of a web application predicting the price of a house based on customized (user-input) characteristics. Data comes from the Kaggle competition House Prices: Advanced Regression Techniques [a link](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

## Getting started
To get this web app up and running, you will need to setup and AWS account to enable the following:
- Sagemaker endpoint (pre-trained Neural Network) for prediction purposes
- Lambda function (lambda/lambda_function.py) useful for preprocessing the user input needed to make predictions
- Gateway API for the front-end to communicate with the lambda function to deliver the predicted price of the user's house

## Deployment
- Run the House prediction jupyter notebook (source folder, requirements.txt and utils.py files have to be in SageMaker Notebook instance too) to go through the end to end solution that goes from data ingestion and pre-processing to training a Neural Network and deploying a SageMaker endpoint. This endpoint will have to be inserted in line 47 of the lambda/lambda_function.py file
- Setup a lambda function [a link](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html) and upload the entire lambda folder in this repo as a zip file. 
- Create a Gateway API with Lambda integration [a link](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html) The API will need to have a POST method and once deployed, its URL will have to be inserted in line 48 of the index.html file.

## Built With
- AWS
- Python
- Javascript
- HTML5, CSS

## Authors
Filippo Giulio Frezza



