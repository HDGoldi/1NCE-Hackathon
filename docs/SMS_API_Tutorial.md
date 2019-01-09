# SMS Howto MO/MT

This is a manual on how to send and receive MO and MT SMS via the 1nce API and what the requirements for this are.

## MO SMS
MO SMS can be forwarded by an SMS gateway via HTTP.

### Client
- Write a script to send SMS via a device employing the sim card
- Requires the SMSC address which can be found in the 1nce portal but is also saved on the sim card and can be read by an AT-command
- International phone number to send the SMS to
    - When forwarding of the SMS is enabled the number is irrelevant
    - Use the MSISDN when communicating P2P

### Forwarding 
- Insert the URI you want to forward your SMS to in the 1nce portal including port and path of your application
    - When using OpenVPN insert the IP of the OpenVPN client e.g. http://10.64.70.198:5000/sms
    - If internet is available use the URI of your application e.g. http://mycoolwebsite.de/sms

### Server
- Provide a REST interface in your application enabling POST requests
- The SMS is forwarded as a JSON via POST

**Headers**
```
Content-Type: application/json
```

**Body**
```json
{
  'multi_part_info': {
    'partno': 1,
    'total': 1,
    'identifier': '6202'
  },
  'payload': 'message text',
  'submit_date': '2018-08-17 16:31:51', // GMT+0
  'dest_address': '882285100000039', // MSISDN in this P2P example
  'organisation': {
    'id': '4567'
  }, 
  'pid': '0',
  'id': '6202',
  'endpoint': {
    'id': '8765432',
    'name': '8988280666000000037' // required to be ICCID for MT SMS via 1nce API!
  },
  'source_address': '882285100000037', // MSISDN of the sending sim
  'dcs': '0'
}
```
- The forwarding server expects a 2xx response after a successful forwarding or else the SMS will be buffered

- When employing OpenVPN add a routing for the SMS gateway server to your client.conf
```
route 10.70.1.14
```

## MT SMS

MT SMS can be send via the 1nce REST API.

### Authentication

In order to use the 1nce REST API the application has to be authenticated first.
To date only authentication via OAuth2 with username and password is implemented.

#### OAuth2
- Authentication is possible with username and password of the 1nce portal with the following workflow
    - Send username and password base64 encoded to the authentication server
    - Get a response including a UUID for authentication
    - Use the UUID to authenticate REST requests
- The UUID for authentication has a short validity period of 240 minutes
- Send the authentication request via POST to
```
https://api.1nce.com/management-api/oauth/token
```

##### Request

**Header**
```json
{
  'Content-Type': 'application/x-www-form-urlencoded', 
  'authorization': 'Basic <base64 encoded username:password>'
}
```

**Body**
```json
{
  'grant_type': 'client_credentials'
}
```

##### Response
```json
{
  "access_token":"6ba7b810-9dad-11d1-80b4-00c04fd430c8", // this is the UUID token you want to use for authentication
  "token_type":"bearer",
  "expires_in":3599,
  "scope":"all",
  "appToken":"<application_token>", // the same as used in the credentials for the OpenVPN
  "userId":<id>,
  "orgId":4321
}
```

#### Application token (Emnify API only, 1nce API tbd)
- Authentication will be possible via the application token found in the 1nce Portal with the following workflow
    - Send application token to the authentication server
    - Receive an authentication token
    - Use the authentication token for REST requests
- The authentication token has a short validity period of 240 minutes
- Send the authentication request via POST to
```
http://dqq7e5l9kxye8.cloudfront.net/api/v1/authenticate
```

##### Request

**Header**
```json
{
  'Content-Type': 'application/json', 
}
```

**Body**
```json
{
  'application_token': '<application_token>' // the same as used in the credentials for the OpenVPN
}
```

##### Response
```json
{
  "auth_token":"<authentication_token>"
}
```

- Send SMS via the Emnify API as stated in their documentation


### Sending MT SMS
- Create an SMS in JSON format including a possible source address and the message
- Send the SMS via POST to the 1nce API with the ICCID of the destination device as a parameter
```
https://api.1nce.com/management-api/v1/sims/<destination ICCID>/sms
```
- Use the authentication UUID to authenticate the application

#### Request

**Header**
```json
{
  'Content-Type': 'application/json',
  'authorization': 'Bearer 6ba7b810-9dad-11d1-80b4-00c04fd430c8', // UUID token gotten from authorization via OAuth2
  'accept': 'application/json'
}
```

**Body**
```json
{
  "payload": "message text",
  "source_address": "882285100000623" // can be set arbitrarily
} 
```

- If successful the server responds with `201 CREATED`

#### Delivery report
The SMS gateway server sends a unsolicited delivery report message after forwarding the SMS to the device.

- Provide a REST interface in your application enabling PATCH requests

**Request**
```json
{
  'status': {
    'status': 'DELIVERED',
    'id': '4'
  },
  'endpoint': {
    'id': '8765432',
    'name': '8988280666000000037'
  }, 
  'submit_date': '2018-08-17 16:46:48',
  'organisation': {
    'id': '4321'
  },
  'final_date': '2018-08-17 16:46:52',
  'id': '6206'
}

```
