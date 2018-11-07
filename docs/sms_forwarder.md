# Setting up SMS Forwarder

For demonstration of the SMS mobile originated we would like to setup the SMS Forwarder for our SIM cards.
Being able to use the feature we need to setup a small backend which is able to handle the SMS messages. 

The 1NCE system can forward MO-SMS to a freely configurable IP/URL. The 1NCE system acts as the HTTPS client. Therefore we must provide an HTTPS server under the specified IP/URL, which is able to receive the requests. 

Example Message send from 1NCE:
```
{
  "dcs": "0",
  "dest_address": "882285000016868",
  "endpoint": {
    "id": "8778667",
    "name": "8988280666000001075"
  },
  "id": "12934",
  "multi_part_info": {
    "identifier": "12934",
    "partno": 1,
    "total": 1
  },
  "organisation": {
    "id": "5136"
  },
  "payload": "Test nach dem Netzwerk ausfallen. SMS geht auf jeden Fall wieder.",
  "pid": "0",
  "smsforwarderId": "1658de33-e7e4-42c1-a885-e733a5d5b43e",
  "source_address": "882285100001075",
  "submit_date": "2018-11-06 08:40:10"
}
```
## Potential Setup for the SMS Forwarder (Example with AWS)

Depending on the use case for Mobile Originating SMS the system layout can be different. For demonstation purposes the following layout is using Amazon Web Service as Backend and main integration layer. This gives a very scalable layout, which can be integrated and further extended very easily. 

![SMS Forwarder Architecture](images/sms-forwarder-setup.png)

Main goal for all SMS Forwarder Applications should be an harmonized backend which can distribute SMS to multiple applications depending on the needs. 

## Building API Gateway in AWS and storing Messages in DynamoDB

Main Goal: Api Gateway -> Lambda (Put) -> DynamoDB

We are going to build a serverless component consisting of:
* an API Gateway, receiving request data
* a Lambda function, that processes that data and saves
* a DynamoDB table, where all your data is stored.

Aside from this main functionality, its important features are:
* Supports CORS
* Written in Node.js
* Easily composable into your other app components by adding triggers to its DynamoDB table

First we need to put together a small Node.js handler for our Lambda function:
```
const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const uuidv4 = require('uuid/v4');
const processResponse = require('./process-response.js');
const TABLE_NAME = process.env.TABLE_NAME;
const IS_CORS = process.env.IS_CORS;
const PRIMARY_KEY = process.env.PRIMARY_KEY;

exports.handler = (event) => {
    if (event.httpMethod === 'OPTIONS') {
		return Promise.resolve(processResponse(IS_CORS));
	}
    if (!event.body) {
        return Promise.resolve(processResponse(IS_CORS, 'invalid', 400));
    }
    let item = JSON.parse(event.body);
    item[PRIMARY_KEY] = uuidv4();
    let params = {
        TableName: TABLE_NAME,
        Item: item
    }
    return dynamoDb.put(params)
    .promise()
    .then(() => (processResponse(IS_CORS)))
    .catch(dbError => {
        let errorResponse = `Error: Execution update, caused a Dynamodb error, please look at your logs.`;
        if (dbError.code === 'ValidationException') {
            if (dbError.message.includes('reserved keyword')) errorResponse = `Error: You're using AWS reserved keywords as attributes`;
        }
        console.log(dbError);
        return processResponse(IS_CORS, errorResponse, 500);
    });
};
```

For easy deployment we are going to use a AWS Template written in YML. 
Everything can be found in the folder ../sms-forwarder.

The whole function is based on the following project: https://github.com/simalexan/api-lambda-save-dynamodb

## Integrating incoming Messages into Application - Example here Zulip Chat Tool
