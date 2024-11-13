from flask import Flask, jsonify, abort, request, make_response, url_for, session
from flask import render_template, redirect
import time
import exifread
import json
import uuid
import boto3
import pymysql.cursors
from datetime import datetime
from pytz import timezone

#------------------change the key,secret-----------------------
# IAM User access configuration
AWS_ACCESS_KEY="key1"
AWS_SECRET_ACCESS_KEY="key2"
AWS_REGION="us-east-1"

#------------------change the bucket-----------------------
# S3 Bucket for csv
PHOTOGALLERY_S3_BUCKET_NAME="ece4150-group-project"

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                   region_name=AWS_REGION)


app = Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/promap')
def proMapPage():
    try:
        #------------------change the csv path-----------------------
        response = s3.get_object(Bucket=PHOTOGALLERY_S3_BUCKET_NAME, Key='result/profit_result_all.csv')
        csv_data = response['Body'].read().decode('utf-8')
        # preprocess the data from csv
        pre_data = []
        for line in csv_data.split('\n')[:]:
            if line:
                locationID, zone, borough, value = line.split(',')
                value = round(float(value), 2)
                pre_data.append({"locationID": int(locationID), "zone": zone, "borough":borough, "value": value})
        # print(pre_data)
        # pass the json data
        return render_template('promap.html', data=pre_data)
    except Exception as e:
        print("Error reading CSV file:", e)
        return "Error reading CSV file"

@app.route('/topdrop')
def topDropPage():
    try:
        #------------------change the csv path-----------------------
        response = s3.get_object(Bucket=PHOTOGALLERY_S3_BUCKET_NAME, Key='result/top100_drop_off.csv')
        csv_data = response['Body'].read().decode('utf-8')
        # preprocess the data from csv
        pre_data = []
        for line in csv_data.split('\n')[:]:
            if line:
                locationID, value, borough = line.split(',')
                pre_data.append({"locationID": int(locationID), "value": int(value), "borough": borough})
        # print(pre_data)
        # pass the json data
        return render_template('topdrop.html', data=pre_data)
    except Exception as e:
        print("Error reading CSV file:", e)
        return "Error reading CSV file"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
