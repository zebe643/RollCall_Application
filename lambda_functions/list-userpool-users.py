import json
import boto3

def lambda_handler(event, context):

    cog_client = boto3.client('cognito-idp')
    ddb_client = boto3.client('dynamodb')

    cognito_response = cog_client.list_users(
        UserPoolId='eu-west-1_i0HfJ8ilR'
    )
    print(cognito_response)
    cog_username = cognito_response
        
    
    ddb_response = ddb_client.scan(
        TableName='LeaveRequests',
        AttributesToGet=[
        'Username',
        'StartDate',
        'EndDate',
        'RequestStatus'
        ]
    )
    print(ddb_response)

    response = cognito_response, ddb_response
 
    newResponse = json.dumps(response, indent=4, sort_keys=True, default=str)
    return newResponse
    
