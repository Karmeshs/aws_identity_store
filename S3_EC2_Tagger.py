# import json
# import boto3
# import logging

# logging.getLogger().setLevel(logging.INFO)
# log = logging.getLogger(__name__)
# # Boto 3 client initialised
# ec2 = boto3.client('ec2')

# def lambda_handler(event, context):
    
#     """
#     This Funtion Searches across all SGs in the account &  region where this lambda exists for any SG ingress rules having the "target_ip",
#     if found it will check if the rule has ports mentioned or not and will make the "revoke_security_group_ingress" to remove the rules with
#     the target_ip.
#     """
    
#     #The ip to check and delete the sg rule if it exists
#     target_ip ="0.0.0.0/0"
    
#     response = ec2.describe_security_groups()
#     #Looping through all SGs
#     print("The Ingress rules with target_ip are as follows: \n")

#     for sg in response['SecurityGroups']:
        
#         # print("Security Group Name: " + sg['GroupName'])
        
#         #Looping through all ingrss rules
#         for ingress in sg['IpPermissions']:

#             #If ports are defined in rule try block executes, it will revoke sg rules with target ip in it
#             try:
#                 for ips in ingress['IpRanges']:
#                     if ips['CidrIp'] == target_ip:
#                         inbound_default_rule = ec2.revoke_security_group_ingress(
#                             IpProtocol=ingress['IpProtocol'],
#                             CidrIp = target_ip,
#                             GroupId = sg['GroupId'],
#                             FromPort=ingress['FromPort'],
#                             ToPort=ingress['ToPort']
#                             )
#                         log.info(f"'Deleting Rule of Security Group Named:': {sg['GroupName']}")
#                         log.info(f"'IP Protocol:': {ingress['IpProtocol']}")
#                         log.info(f"'PORT: ': {str(ingress['FromPort'])}")
#                         log.info(f"'IP Ranges: ': {ips['CidrIp']}")
#                         log.info(f"'Response of revoke_security_group_ingress api call ': {inbound_default_rule}")                    
                                    
#             #If ports are not defined(all traffic) in rule except block executes, it will revoke sg rules with target ip in it
#             except Exception:
#                 print("No value for ports and ip ranges available for this security group rule")
#                 for ips in ingress['IpRanges']:
#                     if ips['CidrIp'] == target_ip:
#                         inbound_default_rule = ec2.revoke_security_group_ingress(
#                             IpProtocol=ingress['IpProtocol'],
#                             CidrIp = target_ip,
#                             GroupId = sg['GroupId']
#                             )
#                         log.info(f"'Deleting Rule of Security Group Named:': {sg['GroupName']}")
#                         log.info(f"'IP Protocol:': {ingress['IpProtocol']}")
#                         log.info(f"'IP Ranges: ': {ips['CidrIp']}")
#                         log.info(f"'Response of revoke_security_group_ingress api call ': {inbound_default_rule}")
#                         continue
            
#     return 0




"""

The function adds tags to the ec2 instances and attached ebs volumes for all the instances
 and to S3 buckets.

Function can be run manually or could be triggered based on cron expression through eventbridge.
"""
import json
import logging
import boto3
import botocore

logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger(__name__)

# Instantiate Boto3 clients & resources for every AWS service API called
ec2_client = boto3.client("ec2")
ec2_resource = boto3.resource("ec2")
s3_resource = boto3.resource('s3')

# Apply resource tags to EC2 instances & attached EBS volumes
def set_ec2_instance_attached_vols_tags(ec2_instance_id, resource_tags):
    """Applies a list of passed resource tags to the Amazon EC2 instance.
       Also applies the same resource tags to EBS volumes attached to instance.

    Args:
        ec2_instance_id: EC2 instance identifier
        resource_tags: a list of key:string,value:string resource tag dictionaries

    Returns:
        Returns True if tag application successful and False if not

    Raises:
        AWS Python API "Boto3" returned client errors
    """
    try:
        response = ec2_client.create_tags(
            Resources=[ec2_instance_id], Tags=resource_tags
        )
        response = ec2_client.describe_volumes(
            Filters=[{"Name": "attachment.instance-id", "Values": [ec2_instance_id]}]
        )
        try:
            for volume in response.get("Volumes"):
                ec2_vol = ec2_resource.Volume(volume["VolumeId"])
                vol_tags = ec2_vol.create_tags(Tags=resource_tags)
            return True
        except botocore.exceptions.ClientError as error:
            log.error(f"Boto3 API returned error: {error}")
            log.error(f"No Tags Applied To: {volume['VolumeId']}")
            return False
    except botocore.exceptions.ClientError as error:
        log.error(f"Boto3 API returned error: {error}")
        log.error(f"No Tags Applied To: {ec2_instance_id}")
        return False

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_s3_tags():
    """
    Adding Tags added to the dictionary "bucket_tags" to all the S3 buckets.
    """
    bucket_tags = []

    bucket_tags.append({"Key": "costcenter", "Value": "XYZ"})
    bucket_tags.append({"Key": "ownername", "Value": "CTO"})
    bucket_tags.append({"Key": "dataclassification", "Value": "confidential"})
    # bucket_tags.append({"Key": "ResourceType", "Value": "S3"})

    for bucket in s3_resource.buckets.all():
        bucket.Tagging().put(Tagging={'TagSet': bucket_tags})
        log.info(f"'Tagged Bucket': {bucket.name}")
        log.info(f"'body': {json.dumps(bucket_tags)}")

    return True

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def lambda_handler(event, context):
    """Making a list of tags "resource_tags" to be applied to resources"""
    # Tag EC2 instances
    resource_tags = []

    resource_tags.append({"Key": "costcenter", "Value": "XYZ"})
    resource_tags.append({"Key": "ownername", "Value": "CEO"})
    resource_tags.append({"Key": "dataclassification", "Value": "confidential"})
    # resource_tags.append({"Key": "ResourceType", "Value": "EC2"})

    for instance in ec2_resource.instances.all():

        #Function call to add tags to ec3 and ebs        
        if set_ec2_instance_attached_vols_tags(instance.id, resource_tags):
            log.info("'statusCode': 200")
            log.info(f"'Resource ID': {instance.id}")
            log.info(f"'body': {json.dumps(resource_tags)}")
        else:
            log.info("'statusCode': 500")
            log.info(f"'No tags applied to Resource ID': {instance.id}")
            log.info(f"'Lambda function name': {context.function_name}")
            log.info(f"'Lambda function version': {context.function_version}")

    #Function call to add tags to S3 buckets 
    set_s3_tags()
    return 0