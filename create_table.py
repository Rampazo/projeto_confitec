import boto3

AWS_ACCESS_KEY_ID = 'AKIA5BNVCCYMPP7XGE2K'
AWS_SECRET_ACCESS_KEY = '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'

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

table = dynamodb.create_table(
    TableName='artist_request',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'artist',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'artist',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.item_count)
