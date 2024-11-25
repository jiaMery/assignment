
import os
import boto3
import json
from typing import Dict, List

def lambda_handler(event, context) -> Dict:
    """
    Get all items from DynamoDB table by partition key task_id
    """
    # Get table name from environment variable
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        # Get task_id from event
        task_id = event['queryStringParameters']['task_id']        
        # Query DynamoDB table
        response = table.query(
            KeyConditionExpression='task_id = :task_id',
            ExpressionAttributeValues={
                ':task_id': task_id
            }
        )
        
        # Return items
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }