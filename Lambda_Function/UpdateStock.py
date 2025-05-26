import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

sns = boto3.client('sns')
TOPIC_ARN = 'arn:aws:sns:us-east-1:827429375794:SellWaiLowStockAlert'  # ใช้ของคุณเอง

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

        #อัปเดต stock
        table.update_item(
            Key={'ProductID': product_id},
            UpdateExpression='SET stock = :s',
            ExpressionAttributeValues={':s': new_stock}
        )

        #ถ้า stock < 5 → แจ้งเตือน
        if new_stock < 5:
            # 🔍 ดึงชื่อสินค้า
            response = table.get_item(Key={'ProductID': product_id})
            item = response.get('Item', {})
            product_name = item.get('name', f'ProductID {product_id}')

            message = f"สินค้า {product_name} เหลือเพียง {new_stock} ชิ้นแล้ว!"
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=message,
                Subject="SellWai - แจ้งเตือนสินค้าใกล้หมดสต๊อก"
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
