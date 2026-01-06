import os
import json
import logging
import sys
from pip._internal import main

main(['install', '-I', '-q','boto3','requests','opensearch-py==2.4.2', 'urllib3','--target', '/tmp/', '--no-cache-dir', '--disable-pip-version-check'])
sys.path.insert(0,'/tmp/')

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from botocore.exceptions import NoCredentialsError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_opensearch_client(endpoint):
    service = "aoss" if "aoss" in endpoint else "es"
    logger.debug(f"Connecting to OpenSearch service: {service} at {endpoint}")
    return OpenSearch(
        hosts=[
            {
                "host": endpoint,
                "port": 443,
            }
        ],
        http_auth=AWSV4SignerAuth(
            boto3.Session().get_credentials(), os.getenv("AWS_REGION"), service
        ),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=10,
    )

def handler(event, context):
    logger.info('Received event: %s', json.dumps(event, indent=2))
    print(event)
    # Parse the JSON string in the Payload field
    #payload_str = event['ResourceProperties']['Create']['parameters']['Payload']
    #payload = json.loads(payload_str) 
    opensearch_endpoint = event['Endpoint']
    index_name = event['IndexName']
    print(opensearch_endpoint)
    opensearch_client = get_opensearch_client(opensearch_endpoint)

    try:
        if event['RequestType'] == 'Create' :

            params = {
                'index': index_name,
                'body': {
                    'settings': {
                        'index': {
                            'knn': True,
                            "knn.algo_param.ef_search": 512
                        }
                    },
                    'mappings': {
                        "properties":
                      {
                          "bedrock-knowledge-base-default-vector":
                          {
                              "type": "knn_vector",
                              "dimension": 1024,
                              "method":
                              {
                                  "name": "hnsw",
                                  "engine": "faiss",
                                  "parameters":
                                  {},
                                  "space_type": "l2"
                              }
                          },
                          "AMAZON_BEDROCK_METADATA\t":
                          {
                              "type": "text",
                              "index": "false"
                          },
                          "AMAZON_BEDROCK_TEXT_CHUNK\t":
                          {
                              "type": "text",
                              "index": "true"
                          }
                      }
                    }
                }
            }

            try:
                opensearch_client.indices.create(index=params['index'], body=params['body'])
            except Exception as e:
                logger.error(e)

        elif event['RequestType'] == 'Delete':
            try:
                opensearch_client.indices.delete(index=index_name)
            except Exception as e:
                logger.error(e)

    except NoCredentialsError:
        logger.error('Credentials not available.')