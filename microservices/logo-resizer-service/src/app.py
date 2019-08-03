import io
import logging
import os
import uuid

import PIL
import boto3
import data as data
from PIL import Image

from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)

basewidth = 300
s3 = boto3.client('s3', region_name='eu-central-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket_url = 'https://aws-the-right-way.s3.eu-central-1.amazonaws.com/logos/'


@app.route('/api/upload_image', methods=['POST'])
def upload_to_s3():
    bucket = 'aws-the-right-way'
    logo_name = uuid.uuid4()
    key = "logos/%s_logo.jpeg" % logo_name
    to_save = request.files['image']

    args = {
        'ContentType': 'image/jpeg',
        'ACL': 'public-read'
    }
    filepath = resize(to_save, str(logo_name))
    s3.upload_file(Filename=filepath, Bucket=bucket, Key=key, ExtraArgs=args)
    push_to_sqs(stock_logo_url=bucket_url + key, stock_name=request.form['name'])
    os.remove(filepath)
    return 'OK'


def resize(image_file, logo_name):
    img = Image.open(image_file)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1] * float(wpercent))))
    resized_image = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    filename = '%s.jpeg' % logo_name
    resized_image.save(filename)
    return filename


def push_to_sqs(stock_logo_url, stock_name):
    sqs = boto3.client('sqs', region_name='eu-central-1', aws_access_key_id='AKIAYVMHSJZU7DONVHQR',
                       aws_secret_access_key='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')

    queue_url = 'https://sqs.eu-central-1.amazonaws.com/595674156649/stock-of-the-day'

    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'StockName': {
                'DataType': 'String',
                'StringValue': stock_name
            },
            'LogoUrl': {
                'DataType': 'String',
                'StringValue': stock_logo_url
            }
        },
        MessageBody=(
            'Information about uploaded Stock Logo and Name'
        )
    )
    print(response['MessageId'])


app.run(host='0.0.0.0', debug=True, port=5001)
