import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Products')  # ชื่อตาราง DynamoDB

def lambda_handler(event, context):
    # รับ query จาก frontend ผ่าน query string เช่น ?query=iphone
    keyword = event.get('queryStringParameters', {}).get('query', '').lower()

    if not keyword:
        return {
            'statusCode': 400,
            'body': 'Missing search query'
        }

    # Scan table แล้ว filter จาก name_lower
    response = table.scan(
        FilterExpression='contains(name_lower, :kw)',
        ExpressionAttributeValues={':kw': keyword}
    )

    # เตรียมผลลัพธ์
    items = response.get('Items', [])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # ถ้าจะใช้กับ frontend
        },
        'body': str(items)
    }
