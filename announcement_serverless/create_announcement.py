import json
import boto3

from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    table_announcements = dynamodb.Table('announcements')

    announcement_title = event['title']
    announcement_description = event['description']
    announcement_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    try:
        table_announcements.put_item(
           Item={
                'title': announcement_title,
                'description': announcement_description,
                'date': announcement_date
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted announcement!')
        }

    except:
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'body': json.dumps('Error saving the announcement')
        }
