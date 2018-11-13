# Sending and receiving SMS (depending on Module)

For demonstration of the using the SMS functionality on our test IoT Gateway (Raspberry PI) we want to be able to send SMS and receive the latest SMS.
Since we are using the Huawei E303 usb modem stick this might be different as in other setups. 
The modem itself is nothing great considering its data capabilities are pretty obsolete. It does have one cool feature. It has a Web GUI for sending and receiving SMS messages, which we can also use via API on the command line.
We want to be able to send text/sms directly from the command line.

## Sending SMS
We need to setup and create our own command to send an SMS via bash. 
This can be done by creating a little bash script which is using the Huawei API.
The script needs to be capable to get different arguments for number and message.
The first argument is the number to send the message to, the second argument is the message itself (make sure you wrap it in quote marks.

We paste the following code into /usr/local/bin/send_sms by using: `sudo nano /usr/local/bin/send_sms`

```bash
#! /bin/bash
hilink_host=192.168.1.1
api_url="http://$hilink_host/api"

curl --data "<request>
         <Index>-1</Index>
         <Phones>
         <Phone>$1</Phone>
         </Phones>
         <Sca></Sca>
         <Content>$2</Content>
         <Length>${#2}</Length>
         <Reserved>1</Reserved>
         <Date>$(date +"%Y-%m-%d %T")</Date>
</request>" $api_url/sms/send-sms
```

To make the send_sms command directly availabe from the command line you also need to run: `sudo chmod +x /usr/local/bin/send_sms`

## Receiving SMS
We want to be able to get the last SMS received easily via command line.

We paste the following code into /usr/local/bin/get_sms by using: `sudo nano /usr/local/bin/get_sms`

```bash
#! /bin/bash
hilink_host=192.168.1.1
api_url="http://$hilink_host/api"

curl --header "X-Requested-With XMLHttpRequest" --data "<request>
         <PageIndex>1</PageIndex>
         <ReadCount>1</ReadCount>
         <BoxType>1</BoxType>
         <SortType>0</SortType>
         <Ascending>0</Ascending>
         <UnreadPreferred>0</UnreadPreferred>
</request>" $api_url/sms/sms-list --silent
```

To make the send_sms command directly availabe from the command line you also need to run: `sudo chmod +x /usr/local/bin/get_sms`