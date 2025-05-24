import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

def default_converter(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError

def lambda_handler(event, context):
    # ลบ space ออกจาก keyword และแปลงเป็น lowercase
    keyword = event.get('queryStringParameters', {}).get('query', '').replace(' ', '').lower()

    if not keyword:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Missing search query'})
        }

    try:
        response = table.scan()
        all_items = response.get('Items', [])

        # ลบ space และ lowercase ทั้งชื่อในตารางกับ keyword ก่อนเปรียบเทียบ
        result = [
            item for item in all_items
            if keyword in item.get("name", "").replace(' ', '').lower()
        ]

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, default=default_converter)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

