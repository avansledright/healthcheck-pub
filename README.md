# Server Status Checker
This script and Lambda function will preform a request on any domain hosted in Route53 with an "A" record. The purpose is to ensure that the web server is returning a value that you intend.

## Usage
To utilize this function you will need to have:
1. SNS setup
2. An active Slack account (if you intend to utilize the Lambda function)
3. Cloudwatch Logs with Log group and Log Stream setup

Modify the sections in "main.py" where you will need to put in the ARN of your SNS topic as well as the name of your Log Group and Log Stream. You can implement this script on any server that can access AWS. Personally I have it running on a local server on a CRON Job. You could run this on an EC2. I choose to run it locally so that testing is done away from AWS.

## Lambda Function
1. Create a new Lambda function
2. Subscribe it to your SNS topic with the proper permissions
3. Modify the function in the ZIP file to have your Slack channel information
4. Create an environment variable for $slackBot with your OAuth token from Slack
5. Upload the entire ZIP file to your lambda function.

The Lambda function will take any inbound message from the SNS topic and publish it to slack with the alert of "SERVER DOWN". You can modify the function as needed. Remember to replace the modified function in the ZIP file and re-upload.

### TO DO
1. Create Terraform scripts to do automated deployment of Lambda, SNS, CloudWatch Logs
