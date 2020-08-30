import json
import uuid
import redis
import boto3
import requests

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from flask import Flask, jsonify, request
from boto3.dynamodb.conditions import Attr
from redis import StrictRedis
from botocore.exceptions import ClientError


app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# API GENIUS PARAMETERS
base_url = 'https://api.genius.com/search/'
client_access_token = 'dnYSJUMeAxJspIw-NtshcskFHnWhZChOcD3ooKEp4hWV7dp72YotrV0_hPFkBQr3'

# Redis Connection
redis_server = redis.Redis("localhost")

# Define cache
cache = StrictRedis()


@app.route('/artist/<name>', methods=['GET'])
def get_artists(name):
    table = dynamodb.Table('artist_request')

    args = request.args
    if 'cache' in args:
        cache_parameter = eval(args['cache'])
    else:
        cache_parameter = True

    # Get item in table
    get_response = table.scan(
        FilterExpression=Attr("artist").eq(name)
    )

    if cache_parameter:

        if get_response.get('Items'):
            # Return Redis response
            res = redis_server.get(get_response.get('Items')[0].get('id'))
        else:
            # Create in DynamoDB Table
            id_uuid = str(uuid.uuid4())
            table.put_item(
                Item={
                    'id': id_uuid,
                    'artist': name
                }
            )

            # Genius Request
            res = request_genius(name).text

            # Save Redis Cache
            redis_server.set(id_uuid, res)

    else:
        if get_response.get('Items'):
            rec_id = get_response.get('Items')[0].get('id')
            # Delete from cache
            cache.delete(rec_id)
            # Delete from DynamoDB
            delete(table, rec_id, name)
        res = request_genius(name).text

    return jsonify(json.loads(res)), 200


def request_genius(q_parameter):
    return requests.get(base_url, params={'q': q_parameter}, headers={'Authorization': f'Bearer {client_access_token}'})


def delete(table, rec_id, artist):
    try:
        response = table.delete_item(
            Key={
                'id': rec_id,
                'artist': artist
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response


if __name__ == '__main__':
    app.run(debug=True)
