import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ClaimsTable')

def send_response_to_claim_processor(claim_id, status, message):
    # Mock function to send response back to claim processor
    print(f"Claim ID: {claim_id}, Status: {status}, Message: {message}")

def notify_user(user_id, message):
    # Mock function to notify the user
    print(f"User ID: {user_id}, Message: {message}")

def store_claim_in_dynamodb(claim_id, status, reason=None):
    table.put_item(
        Item={
            'ClaimID': claim_id,
            'Status': status,
            'Reason': reason,
            'Timestamp': datetime.utcnow().isoformat()
        }
    )

def check_claim_history(user_id, months):
    # Mock function to check claim history
    # Returns True if no claims in the last 'months' months
    return True

def get_vendor_claims(vendor_id, days):
    # Mock function to get the number of claims for a vendor in the last 'days' days
    return 5

def lambda_handler(event, context):
    claim_id = event['claim_id']
    transaction_date = datetime.strptime(event['transaction_date'], '%Y-%m-%d')
    transaction_amount = event['transaction_amount']
    user_id = event['user_id']
    vendor_id = event['vendor_id']

    # Rule 1: Transaction from less than 30 days
    if (datetime.utcnow() - transaction_date).days > 30:
        reason = "Transaction is older than 30 days"
        store_claim_in_dynamodb(claim_id, "Rejected", reason)
        notify_user(user_id, reason)
        send_response_to_claim_processor(claim_id, "Rejected", reason)
        return
    
    # Rule 2: Transaction amount < 50
    if transaction_amount < 50:
        store_claim_in_dynamodb(claim_id, "Approved")
        send_response_to_claim_processor(claim_id, "Approved", "No issues")
        return
    
    # Rule 3: Transaction amount > 100 and no claim history in 6 months
    if transaction_amount > 100 and not check_claim_history(user_id, 6):
        store_claim_in_dynamodb(claim_id, "Approved")
        send_response_to_claim_processor(claim_id, "Approved", "No claim history in 6 months")
        return
    elif transaction_amount > 100:
        reason = "Exceeded the number of claims within 30 days"
        store_claim_in_dynamodb(claim_id, "Rejected", reason)
        notify_user(user_id, reason)
        send_response_to_claim_processor(claim_id, "Rejected", reason)
        return

    # Rule 4: Transaction amount > 1000, no claim history in 6 months, and same day claim
    if transaction_amount > 1000 and not check_claim_history(user_id, 6) and (datetime.utcnow() - transaction_date).days == 0:
        if get_vendor_claims(vendor_id, 30) > 10:
            reason = "Vendor has over 10 claims in 30 days"
            store_claim_in_dynamodb(claim_id, "Rejected", reason)
            notify_user(user_id, reason)
            send_response_to_claim_processor(claim_id, "Rejected", reason)
            return
        store_claim_in_dynamodb(claim_id, "Approved")
        send_response_to_claim_processor(claim_id, "Approved", "Claim made on same day of transaction")
        return

    # If none of the rules apply, reject the claim
    reason = "Failed all rules"
    store_claim_in_dynamodb(claim_id, "Rejected", reason)
    notify_user(user_id, reason)
    send_response_to_claim_processor(claim_id, "Rejected", reason)
-------------------------------------------------------------------------------------------------------------------------
