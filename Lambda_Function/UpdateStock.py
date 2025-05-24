import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        product_id = body.get('ProductID')
        new_stock = int(body.get('stock'))

        if not product_id or new_stock < 0:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing or invalid data'})
            }

        table.update_item(
            Key={'ProductID': product_id},
            UpdateExpression='SET stock = :s',
            ExpressionAttributeValues={':s': new_stock}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Stock updated for {product_id}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
