import json
import boto3
import urllib
import urllib.parse
import ast
s3 = boto3.client("s3")
client = boto3.client('pinpoint-email')

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        filename = str(file_obj['s3']['object']['key'])
        bucketname = event["Records"][0]['s3']['bucket']['name']
        filename = urllib.parse.unquote_plus(filename)
        print("Filename: ", filename)
        print("BucketName: ", bucketname)
        print("Making object public-read")
        
    response = s3.put_object_acl(
        ACL="public-read",
        Bucket= bucketname,
        Key=filename
    )
    
    fileObj = s3.get_object(Bucket = bucketname, Key=filename)
    file_content = json.loads(fileObj['Body'].read())
    str(file_content)
    print(file_content)
    
    User = file_content['User']
    Psprofile = file_content['Psprofile']
    Requesttype = file_content['Requesttype']
    Shift = file_content['Shift']
    Dayshift = file_content['Dayshift']
    Startdate = file_content['Startdate']
    Enddate = file_content['Enddate']
    Requestreason = file_content['Requestreason']
    decodedRReason = urllib.parse.unquote(Requestreason)
    Site = file_content['Site']
    rosterOwner = "burnz@amazon.com"
    
    response = client.send_email(
        FromEmailAddress="aws-ps-rollcall@amazon.com",
        Destination={
            "ToAddresses":[
                rosterOwner
                ],
        },Content={
            "Simple": {
                "Subject": {
                    "Data": "Rollcall:[" + Requesttype + "][" + User + "][" + Startdate +"]",
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": "Hi," + "\n\n" + "I'm requesting some time off for the reason: " + Requesttype + ".\n" + "My shift for the week is " + Shift + ".\n" +
                        "The first date I need off is " + Startdate + " and the last day is " + Enddate + "." + ".\n\n" +  "PS Profile: " + Psprofile + "\n\n" + "Additional Information: " + decodedRReason +
                        "\n\n" + "Many thanks," + "\n" + User,
                        "Charset": "UTF-8"
                    }
                }
            }
        }
    )
    print(response)