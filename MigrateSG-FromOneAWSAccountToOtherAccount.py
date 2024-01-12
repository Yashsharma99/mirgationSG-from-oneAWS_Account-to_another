
###########################################################################
## Created by: Yash Sharma                                               ##
## Date:       19/July/2023                                             ##
## Team:       R&D Tools Team                                            ##
## To migrate security groups from one AWS account to another AWS account##
###########################################################################


import boto3

sourceAccount={
        'AccessKey':'<SOURCE-ACCOUNT_ACCESS_KEY>',
        'SecretKey':'<SOURCE-ACCOUNT_SECRET_KEY>',
        'Region':'eu-central-1',
        'SecurityGroupId':'<Security-GroupID>'
        }
destinationAccount={
        'AccessKey':'<DESTINATION-ACCOUNT_ACCESS_KEY>',
        'SecretKey':'<DESTINATION-ACCOUNT_SECRET_KEY>',
        'Region':'eu-central-1'
        }

# ------ Source Account ------ #

#set up boto3 client for source account

client = boto3.client(
        "ec2",
        region_name = sourceAccount['Region'],
        aws_access_key_id=sourceAccount['AccessKey'],
        aws_secret_access_key=sourceAccount['SecretKey']
        )

# describe security group that will be copied

response = client.describe_security_groups(
        GroupIds=[
                sourceAccount['SecurityGroupId']
                ]
        )["SecurityGroups"][0]

# extract ingress and egress rules for the security group

ingress = response["IpPermissions"]
egress = response["IpPermissionsEgress"]

# ------ Destination Account ------ #

#set up boto3 client for destination account

client = boto3.client(
        "ec2",
        region_name = destinationAccount['Region'],
        aws_access_key_id=destinationAccount['AccessKey'],
        aws_secret_access_key=destinationAccount['SecretKey']
        )

# create a new security group in the destination account

groupId = client.create_security_group(
        Description='security-group-from-{}'.format(sourceAccount['Region']),
        GroupName='<ENTER THE GROUP NAME',
        VpcId='<VPC_ID'
        )["GroupId"]

# removed all egress rules from newly created security group

clearEgress = client.describe_security_groups(
        GroupIds=[groupId]
        )["SecurityGroups"][0]["IpPermissionsEgress"]

client.revoke_security_group_egress(
        GroupId=groupId,
        IpPermissions=clearEgress
        )

# create ingress and egress rules for the newly created security group

client.authorize_security_group_ingress(
        GroupId=groupId,
        IpPermissions=ingress
        )
client.authorize_security_group_egress(
        GroupId=groupId,
        IpPermissions=egress
        )
