import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_announcements = dynamodb.Table('announcements')

    response = table_announcements.scan()

    return {
      'statusCode': 200,
      'body': response['Items']
    }
