import boto3

sqs = boto3.client('sqs', region_name='eu-central-1', aws_access_key_id='AKIAYVMHSJZU7DONVHQR',
                   aws_secret_access_key='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')
queue_url = 'https://sqs.eu-central-1.amazonaws.com/595674156649/stock-of-the-day'


# def process_message():
