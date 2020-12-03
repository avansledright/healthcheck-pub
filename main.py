import boto3
import requests
import os
import time


#aws variables
sns = boto3.client('sns')
aws = boto3.client('route53')
cw = boto3.client('logs')
paginator = aws.get_paginator('list_resource_record_sets')
response = aws.list_hosted_zones()
hosted_zones = response['HostedZones']
time_now = int(round(time.time() * 1000))

#create empty lists
zone_id_to_test = []
dns_entries = []
zones_with_a_record = []
#Create list of ZoneID's to get record sets from       
for key in hosted_zones:
    zoneid = key['Id']
    final_zone_id = zoneid[12:]
    zone_id_to_test.append(final_zone_id)

#Create ZoneID List    
def getARecord(zoneid):
    for zone in zoneid:
        try:
            response = paginator.paginate(HostedZoneId=zone)
            for record_set in response:
                dns = record_set['ResourceRecordSets']
                dns_entries.append(dns)

        except Exception as error:
            print('An Error')
            print(str(error))
            raise
#Get Records to test
def getCNAME(entry):
    for dns_entry in entry:
        for record in dns_entry:
            if record['Type'] == 'A':
                url = (record['Name'])
                final_url = url[:-1]
                zones_with_a_record.append(f"https://{final_url}")
#Send Result to SNS                
def sendToSNS(messages):
    message = messages
    try:
        send_message = sns.publish(
            TargetArn='arn:aws:sns:us-west-2:481692562261:sns_to_slack',
            Message=message,
            )
    except:
        print("something didn't work")
def tester(urls):
    for url in urls:
        try:
            user_agent = {'User-agent': 'Mozilla/5.0'}
            status = requests.get(url, headers = user_agent, allow_redirects=True)
            code = (status.status_code)
            if code == 401:
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
            elif code == 301:
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
            elif code == 302:
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
            elif code == 403:
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
            elif code !=200:
                sendToSNS(f"The site {url} reports: {code}")
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
            else:
                response = f"The site {url} reports status code: {code}"
                writeLog(response)
        except:
            sendToSNS(f"The site {url} failed testing")
            response = f"The site {url} reports status code: {code}"
            writeLog(response)

def writeLog(message):
    getToken = cw.describe_log_streams(
        logGroupName='healthchecks',   
        )
    logInfo = (getToken['logStreams'])
    nextToken = logInfo[0]['uploadSequenceToken']
    response = cw.put_log_events(
        logGroupName='healthchecks',
        logStreamName='serverChecks',
        logEvents=[
            {
                'timestamp': time_now,
                'message': message
            },
        ],
        sequenceToken=nextToken
    )
#Execute            
getARecord(zone_id_to_test)
getCNAME(dns_entries)
zones_with_a_record.remove("https://home.vansledright.com")
zones_with_a_record.remove("https://home.45sq.com")
zones_with_a_record.remove("https://staging.plugins.trueterpenes.com")
tester(zones_with_a_record)

