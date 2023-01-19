# ami-cross-region-replication

## Description: 

 Lambda function that copies all Amazon Machine Images (AMIs) that are 7 days old or older to another region using the boto3 library.
 
 ## Usage Instructions:
 
 This script will copy all the AMIs that are 7 days old or older based on the CreationDate of the AMI. As before make sure that the function has the   necessary permissions to copy AMIs to another region and to access the AMIs.
