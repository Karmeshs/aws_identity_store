import json
import boto3

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
    for sg in response['SecurityGroups']:
        
        print("Security Group Name: " + sg['GroupName'])
        print("The Ingress rules are as follows: \n")
        
        #Looping through all ingrss rules
        for ingress in sg['IpPermissions']:
            
            print("IP Protocol: " + ingress['IpProtocol'])
            
            #If ports are defined in rule try block executes, it will revoke sg rules with target ip in it
            try:
                print("PORT: " + str(ingress['FromPort']))
                for ips in ingress['IpRanges']:
                    print("IP Ranges: " + ips['CidrIp'])
                    if ips['CidrIp'] == target_ip:
                        inbound_default_rule = ec2.revoke_security_group_ingress(
                            IpProtocol=ingress['IpProtocol'],
                            CidrIp = target_ip,
                            GroupId = sg['GroupId'],
                            FromPort=ingress['FromPort'],
                            ToPort=ingress['ToPort']
                            )
                        print("\n\t",inbound_default_rule,"\nDELETED !!")
            
            #If ports are not defined(all traffic) in rule except block executes, it will revoke sg rules with target ip in it
            except Exception:
                print("No value for ports and ip ranges available for this security group")
                for ips in ingress['IpRanges']:
                    print("IP Ranges: " + ips['CidrIp'])
                    if ips['CidrIp'] == target_ip:
                        inbound_default_rule = ec2.revoke_security_group_ingress(
                            IpProtocol=ingress['IpProtocol'],
                            CidrIp = target_ip,
                            GroupId = sg['GroupId']
                            )
                        print("\n\t",inbound_default_rule,"\nDELETED FROM EXCEPT BLOCK !!")
                continue
            
    return 0