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