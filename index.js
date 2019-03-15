
exports.handler = function(event, context, callback) {
console.log(event);
var AWS = require('aws-sdk');
AWS.config.update({region: 'eu-west-1'});
var pinpointemail = new AWS.PinpointEmail({apiVersion: '2018-07-26'});
const rosterOwner = "burnz@amazon.com"

function requestLeave(alias, psprofile, RequestType, MyShift, StartDate, Duration, RequestReason){

    var confirmationEmail = {
        Content: {
            Simple: {
                Body: {
                    Text: {
                        Data: "Hi," + "\n\n" + "I'm requesting some time off for the reason: " + RequestType + ".\n" + "My shift for the week is " + MyShift + ".\n" +
                        "The first date I need off is " + StartDate + " for a total of " + Duration + " days" + ".\n\n" +  "PS Profile: " + psprofile + "\n\n" + "Additional Information: " + unEscRReason.replace(/%20/g, " ") +
                        "\n\n" + "Many thanks," + "\n" + alias,
                        Charset: "UTF-8"
                    }
                },
                  Subject: {
                  Data: "Rollcall:[" + RequestType + "][" + alias + "][" + StartDate +"]" ,
                        Charset: "UTF-8"           
            }
        }
    },
        Destination: {
            //CcAddresses: [alias + "@amazon.com"],
            ToAddresses: 
                [rosterOwner] //will be set as aws-ps-dms-dub-vacation in prod, sent to burnz@amazon.com in dev/beta
        },
        FromEmailAddress: "aws-ps-rollcall@amazon.com"
    };

    pinpointemail.sendEmail(confirmationEmail, function(err, data) {
        if (err) console.log(err, err.stack); //error occured
        else console.log(data); //successful response
    });
}

for(var key in event){
    var user = event["user"]
    var psProfile = event["psprofile"]
    var rType = event["requestType"]
    var shift = event["shift"]
    var sDate = event["startdate"]
    var dur = event["Duration"]
    var rReason = event["RequestReason"]
    var site = event["Site"]
    var dshift = event["dayShift"]   
}





var unEscRReason = unescape(rReason);


requestLeave(user, psProfile, rType, shift, sDate, dur, rReason);
};
