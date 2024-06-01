import json
import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
claim_table = dynamodb.Table('ClaimTable')

def lambda_handler(event, context):
    try:
        # Extract claim details from the event
        transaction_id = event.get('transaction_id')
        claim_amount = event.get('ClaimAmount')
        claim_reason = event.get('claim_reason')
        vendor_claims = event.get('vendor_claims', {})
        vendor_name = vendor_claims.get('vendor_name')
        credit_card = vendor_claims.get('credit_card')
        exp_date = vendor_claims.get('exp_date')
        
        # Claim processing logic (dummy logic for approval)
        claim_status = "processed"
        
        # Create a claim record
        claim_record = {
            'transaction_id': transaction_id,
            'ClaimAmount': claim_amount,
            'claim_reason': claim_reason,
            'vendor': vendor_name,
            'status': claim_status,
            # Avoid storing sensitive information directly
            'exp_date': exp_date
        }
        
        # Store the claim record in DynamoDB
        claim_table.put_item(Item=claim_record)
        
        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'claim_status': claim_status
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
