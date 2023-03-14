import json
import boto3
import logging

logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger(__name__)
# Boto 3 client initialised
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    
    """
    This Funtion Searches across all SGs in the account &  region where this lambda exists for any SG ingress rules having the "target_ip",
    if found it will check if the rule has ports mentioned or not and will make the "revoke_security_group_ingress" to remove the rules with
    the target_ip.
    """
    
    #The ip to check and delete the sg rule if it exists
    target_ip ="0.0.0.0/0"
    
    response = ec2.describe_security_groups()
    #Looping through all SGs
    print("The Ingress rules with target_ip are as follows: \n")

    for sg in response['SecurityGroups']:
        
        # print("Security Group Name: " + sg['GroupName'])
        
        #Looping through all ingrss rules
        for ingress in sg['IpPermissions']:

            #If ports are defined in rule try block executes, it will revoke sg rules with target ip in it
            try:
                for ips in ingress['IpRanges']:
                    if ips['CidrIp'] == target_ip:
                        inbound_default_rule = ec2.revoke_security_group_ingress(
                            IpProtocol=ingress['IpProtocol'],
                            CidrIp = target_ip,
                            GroupId = sg['GroupId'],
                            FromPort=ingress['FromPort'],
                            ToPort=ingress['ToPort']
                            )
                        log.info(f"'Deleting Rule of Security Group Named:': {sg['GroupName']}")
                        log.info(f"'IP Protocol:': {ingress['IpProtocol']}")
                        log.info(f"'PORT: ': {str(ingress['FromPort'])}")
                        log.info(f"'IP Ranges: ': {ips['CidrIp']}")
                        log.info(f"'Response of revoke_security_group_ingress api call ': {inbound_default_rule}")                    
                                    
            #If ports are not defined(all traffic) in rule except block executes, it will revoke sg rules with target ip in it
            except Exception:
                print("No value for ports and ip ranges available for this security group rule")
                for ips in ingress['IpRanges']:
                    if ips['CidrIp'] == target_ip:
                        inbound_default_rule = ec2.revoke_security_group_ingress(
                            IpProtocol=ingress['IpProtocol'],
                            CidrIp = target_ip,
                            GroupId = sg['GroupId']
                            )
                        log.info(f"'Deleting Rule of Security Group Named:': {sg['GroupName']}")
                        log.info(f"'IP Protocol:': {ingress['IpProtocol']}")
                        log.info(f"'IP Ranges: ': {ips['CidrIp']}")
                        log.info(f"'Response of revoke_security_group_ingress api call ': {inbound_default_rule}")
                        continue
            
    return 0