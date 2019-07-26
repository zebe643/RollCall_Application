import json
import boto3
import time

def lambda_handler(event, context): 
    print(event)
    if event:
        body = json.loads(event['body'])
        region = body['Site']
        PsProfile = body['psprofile']
        user = body['user']
        apigwid = event['requestContext']['requestId']
        rtype = body['requestType']
        s = body['shift']
        ds = body['dayShift']
        sd = body['startdate']
        ed = body['enddate']
        site = body['Site']
        rr = body['RequestReason']
        
    jsonObj = {
        "Region": region,
        "Psprofile": PsProfile,
        "User": user,
        "APIGWID": apigwid,
        "Requesttype": rtype,
        "Shift": s,
        "Dayshift": ds,
        "Startdate": sd,
        "Enddate": ed,
        "Site": site,
        "Requestreason": rr
    }
    
    dynamoObj = {
        'Username': {
            'S': user
        },
        'StartDate':{
            'S': sd
        }, 
        'EndDate':{
            'S': ed
        },
        'Region':{
            'S': region
        },
        'PsProfile':{
            'S': PsProfile
        },        
        'APIGWID':{
            'S': apigwid
        },
        'RequestType':{
            'S': rtype
        },
        'Shift':{
            'S': s
        },
        'Dayshift':{
            'S': ds
        },
        'Site':{
            'S': site
        },
        'RequestReason':{
            'S': rr
        },
        'RequestStatus':{
            'S': '1'
        }
    }
    print(jsonObj)
        
    ts = time.time()
    nodec = int(ts)
    
    s3 = boto3.resource('s3')
    obj = s3.Object('leave-requests', apigwid + '_' + user + '_' + PsProfile + '_' + region + '_' + str(nodec) + '.json')
    s3response = obj.put(Body = json.dumps(jsonObj))
    
    client = boto3.client('dynamodb')
    response = client.put_item(
    TableName = 'LeaveRequests',
    Item = dynamoObj
    )
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        
        "body": json.dumps(s3response),
        "isBase64Encoded": False
    }
    print(response)
    return response
   