import json
import boto3
from datetime import datetime

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
transaction_table = dynamodb.Table('TransactionTable')

def lambda_handler(event, context):
    try:
        # Extract transaction details from the event
        transaction_id = event['transaction_id']
        user_name = event['UserName']
        amount = event['amount']
        item_name = event['item_name']
        vendor = event['vendor']
        credit_card = event['credit_card']  # Avoid storing this directly
        exp_date = event['exp_date']
        cvc = event['CVC']
        date_time = event['datetime']
        
        # Transaction processing logic (dummy logic for approval)
        transaction_status = "approved"  # This should be determined by actual payment processing logic
        
        # Create a transaction record
        transaction_record = {
            'transaction_id': transaction_id,
            'UserName': user_name,
            'amount': amount,
            'item_name': item_name,
            'vendor': vendor,
            'datetime': date_time,
            'status': transaction_status
            # Sensitive information like credit_card, exp_date, and CVC should not be stored
        }
        
        # Store the transaction record in DynamoDB
        transaction_table.put_item(Item=transaction_record)
        
        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'transaction_status': transaction_status
            })
        }
    
    except Exception as e:
        # Return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
