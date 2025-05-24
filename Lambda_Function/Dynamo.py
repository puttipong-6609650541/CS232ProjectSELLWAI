import boto3
import json
from decimal import Decimal

# Helper function to convert Decimal to int/float
def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        # เลือก float ถ้าเป็นราคาหรือจำนวนเงิน
        return float(obj)
    else:
        return obj

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

def lambda_handler(event, context):
    response = table.scan()
    items = response['Items']
    clean_items = convert_decimal(items)

    return {
        'statusCode': 200,
        'body': json.dumps(clean_items)
    }