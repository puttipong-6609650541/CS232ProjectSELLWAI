import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

sns = boto3.client('sns')
TOPIC_ARN = 'arn:aws:sns:us-east-1:905418289020:low-stock-alerts' #ARN

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        product_id = body.get('product_id')  
        new_stock = int(body.get('stock'))

        if not product_id or new_stock < 0:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing or invalid data'})
            }

        table.update_item(
            Key={'product_id': product_id},  
            UpdateExpression='SET stock = :s',
            ExpressionAttributeValues={':s': new_stock}
        )

        if new_stock < 5: 
            message = f"สินค้า ProductID '{product_id}' เหลือเพียง {new_stock} ชิ้นแล้ว!"
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=message,
                Subject="แจ้งเตือนสินค้าใกล้หมดสต๊อก"
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
