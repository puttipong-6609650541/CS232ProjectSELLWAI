import boto3
import re
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

def lambda_handler(event, context):
    try:
        #ดึงรายการทั้งหมด
        response = table.scan()
        items = response.get('Items', [])

        #หา ProductID ล่าสุด แล้ว +1
        ids = []
        for item in items:
            pid = item.get('ProductID', '')
            match = re.match(r'^P(\d+)$', pid)
            if match:
                ids.append(int(match.group(1)))

        next_id = max(ids) + 1 if ids else 1
        new_id = f'P{str(next_id).zfill(3)}'  # ✅ แปลงเป็น P001, P002, ...

        #รับข้อมูลจาก body
        body = json.loads(event['body'])
        name = body.get('name')
        category = body.get('category')
        price = body.get('price')
        stock = body.get('stock')

        #Insert ลง DynamoDB
        table.put_item(Item={
            'ProductID': new_id,
            'name': name,
            'category': category,
            'price': price,
            'stock': stock
        })

        return {
            'statusCode': 200,
            'body': json.dumps({ "message": "✅ เพิ่มสินค้าแล้ว", "ProductID": new_id })
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({ "error": str(e) })
        }