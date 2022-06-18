#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from flask_cors import CORS
import boto3
import requests
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import simplejson as json
import uuid

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    

# GET JOBS OF USER


@application.route('/get_jobs', methods=['GET'])
def get_jobs():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    response = table.scan()
    jobs = response['Items']

    return Response(json.dumps(jobs), mimetype='application/json', status=200)    
    
# TEST -
# curl http://localhost:8000/get_jobs




# ADD JOB

@application.route('/add_job', methods=['POST'])
def add_job():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    job_id = (str(uuid.uuid4()))
    data['job_id'] = job_id
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "1"}' http://localhost:8000/add_job


# ADD DEPARTMENTS

@application.route('/add_department', methods=['POST'])
def add_department():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('departments')
    department_id = (str(uuid.uuid4()))
    data['department_id'] = department_id
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "1"}' http://localhost:8000/add_department



# GET DEPARTMENTS1


@application.route('/get_departments', methods=['GET'])
def get_departments():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('departments')
    response = table.scan()
    departments = response['Items']

    return Response(json.dumps(departments), mimetype='application/json', status=200)    
    
# TEST -
# curl http://localhost:8000/get_departments

# S3 - UPLOAD IMAGE
@application.route('/upload_image', methods=['POST'])
def upload_image():
    bucket = 'jce-cloud-project'
    img = request.files['img']
    s3 = boto3.resource('s3', region_name='us-east-1')
    img_path  = "images/%s.jpg" %  (str(uuid.uuid4()))
    s3.Bucket(bucket).upload_fileobj(img, img_path, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}) 
    img_url = 'https://jce-cloud-project.s3.amazonaws.com/'+ img_path
    
    
    rekognition = boto3.client("rekognition", region_name = 'us-east-1')
    
    key = img_path

    response = rekognition.detect_faces(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        }
    }
    )
    
    
    print(response['FaceDetails'][0]['Confidence'])
    confidence = response['FaceDetails'][0]['Confidence'];

    return {"img_url": img_url, "confidence": confidence}
 
 
 # S3 - UPLOAD RESUME (PDF)
@application.route('/upload_resume', methods=['POST'])
def upload_resume():
    bucket = 'jce-cloud-project'
    resume = request.files['resume']
    s3 = boto3.resource('s3', region_name='us-east-1')
    resume_path  = "resumes/%s.pdf" %  (str(uuid.uuid4()))
    s3.Bucket(bucket).upload_fileobj(resume, resume_path, ExtraArgs={'ACL': 'public-read'}) 
    resume_url = 'https://jce-cloud-project.s3.amazonaws.com/'+ resume_path
    
    return {"resume_url": resume_url}
 

 # DynamoDB - ADD APPLICATION 

@application.route('/add_application', methods=['POST'])
def add_add_application():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('job_applications')
    application_id = (str(uuid.uuid4()))
    data['application_id'] = application_id
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"application_id": "1"}' http://localhost:8000/add_application


if __name__ == '__main__':
    flaskrun(application)
