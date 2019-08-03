import os
import time

import boto3
from boto3.dynamodb.conditions import Attr
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sqs = boto3.resource('sqs', region_name='eu-central-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
table = dynamodb.Table('stocks')

queue = sqs.get_queue_by_name(QueueName='stock-of-the-day')


def monitor_queue():
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['StockName', 'LogoUrl']):
        # Get the custom author message attribute if it was set
        if message.message_attributes is not None:
            stock_name = message.message_attributes.get('StockName').get('StringValue')
            logo_url = message.message_attributes.get('LogoUrl').get('StringValue')
            update_dynamo_item(stock_name, logo_url)

        # Let the queue know that the message is processed
        message.delete()


def update_dynamo_item(stock_name, logo_url):
    stock_id = get_id(stock_name)
    table.update_item(
        Key={
            'stock_id': stock_id
        },
        UpdateExpression="set logo_url = :l",
        ExpressionAttributeValues={
            ':l': logo_url
        },
        ReturnValues="UPDATED_NEW"
    )


def get_id(stock_name):
    filter_expression = Attr('name').eq(stock_name)

    response = table.scan(
        FilterExpression=filter_expression
    )

    response = response['Items'][0]
    return response['stock_id']


while True:
    print("Checking for new messages to process ... ")
    monitor_queue()
    time.sleep(1)
