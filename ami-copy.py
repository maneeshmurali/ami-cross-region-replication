import boto3
import datetime

def lambda_handler(event, context):
    # Define the source and destination regions
    source_region = 'us-west-1'
    destination_region = 'us-east-1'

    # Define the age of the AMIs to be copied (in days)
    age_in_days = 7

    # Create a boto3 client for EC2 in the source region
    ec2_client = boto3.client('ec2', region_name=source_region)

    # Get the current time
    now = datetime.datetime.now()

    # Retrieve all AMIs in the source region
    response = ec2_client.describe_images(Owners=['self'])
    images = response['Images']

    # Iterate through the AMIs and copy those that are older than the specified age
    for image in images:
        creation_date = datetime.datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        age = (now - creation_date).days

        if age >= age_in_days:
            source_ami = image['ImageId']
            destination_ami_name = 'Copy of ' + image.get('Name', '')
            description = image.get('Description', '')
            tags = image.get('Tags', [])
            block_device_mappings = image.get('BlockDeviceMappings', [])

            # Create a boto3 client for EC2 in the destination region
            ec2_client = boto3.client('ec2', region_name=destination_region)

            # Copy the source AMI to the destination region
            response = ec2_client.copy_image(
                Name=destination_ami_name,
                Description=description,
                SourceImageId=source_ami,
                SourceRegion=source_region
            )

            # Get the ID of the destination AMI
            destination_ami = response['ImageId']

            # Create tags for the destination AMI
            ec2_client.create_tags(Resources=[destination_ami], Tags=tags)

            # Create block device mappings for the destination AMI
            for bdm in block_device_mappings:
                ec2_client.create_image(
                    Name=destination_ami_name,
                    BlockDeviceMappings=[bdm],
                    DryRun=False,
                    ImageId=destination_ami
                )
