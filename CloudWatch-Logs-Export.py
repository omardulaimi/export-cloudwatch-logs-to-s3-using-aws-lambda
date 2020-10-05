import boto3
import os
import datetime


"""
This portion will obtain the Environment variables from AWS Lambda.
"""

GROUP_NAME = os.environ['GROUP_NAME']
DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']
PREFIX = os.environ['PREFIX']
NDAYS = os.environ['NDAYS']
nDays = int(NDAYS)


"""
This portion will receive the nDays value (the date/day of the log you want
want to export) and calculate the start and end date of logs you want to
export to S3. Today = 0; yesterday = 1; so on and so forth...
Ex: If today is April 13th and NDAYS = 0, April 13th logs will be exported.
Ex: If today is April 13th and NDAYS = 1, April 12th logs will be exported.
Ex: If today is April 13th and NDAYS = 2, April 11th logs will be exported.
"""

currentTime = datetime.datetime.now()
StartDate = currentTime - datetime.timedelta(days=nDays)
EndDate = currentTime - datetime.timedelta(days=nDays - 1)


"""
Convert the from & to Dates to milliseconds
"""

fromDate = int(StartDate.timestamp() * 1000)
toDate = int(EndDate.timestamp() * 1000)


"""
The following will create the subfolders' structure based on year, month, day
Ex: BucketNAME/LogGroupName/Year/Month/Day
"""


BUCKET_PREFIX = os.path.join(PREFIX, StartDate.strftime('%Y{0}%m{0}%d').format(os.path.sep))


"""
Based on the AWS boto3 documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_export_task
"""


def lambda_handler(event, context):
    client = boto3.client('logs')
    client.create_export_task(
         logGroupName=GROUP_NAME,
         fromTime=fromDate,
         to=toDate,
         destination=DESTINATION_BUCKET,
         destinationPrefix=BUCKET_PREFIX
        )