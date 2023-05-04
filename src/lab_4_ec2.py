# Importing libraries for interaction with AWS
from botocore.exceptions import ClientError

# Import utils for load config
from src.utils import load_config

CONFIG = load_config()


def create_instance(ec2_client):
    """
    Create EC2 instance on AWS EC2 server through boto3 client command;
    :param ec2_client: boto3 client connection with ec2 service;
    :return: Name of the instance which was created.
    """
    # Define parameters for creation
    ami_id = "ami-0ec7f9846da6b0f61"
    instance_type = "t2.micro"
    key_name = CONFIG.key_pairs.name
    sec_group_ids = [CONFIG.boto.sec_group_id]
    sec_group_names = [CONFIG.boto.sec_group_name]
    # Try creation
    try:
        instances = ec2_client.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            SecurityGroupIds=sec_group_ids,
            SecurityGroups=sec_group_names,
            KeyName=key_name
        )
        print("Instance create successfully!!")
        print(f"with id: {instances['Instances'][0]['InstanceId']}")
        return instances['Instances'][0]["InstanceId"]
    except ClientError as e:
        print(f"Creation Failed because: {e}")


def instance_manipulation(ec2_client, instance_id='', action="start"):
    """
    Granting access to manipulation to EC2 instance;
    :param ec2_client: boto3 client connection with ec2 service;
    :param instance_id: instance id for manipulation;
    :param action: action name which needs to be done with ec2 instance.
    """
    try:
        match action:
            case "start":
                ec2_client.start_instances(InstanceIds=[instance_id])
                print("Instance starts successfully!")
            case "stop":
                ec2_client.stop_instances(InstanceIds=[instance_id])
                print("Instance stops successfully!")
            case "reboot":
                ec2_client.reboot_instances(InstanceIds=[instance_id])
                print("Instance start rebooting successfully!")
            case _: print("Please choose available actions [start|stop|reboot].")
    except ClientError as e:
        print(f"Action not execute because: {e}")


def get_instance_base_info(ec2_client, instance_id):
    """
    Printing basic info about instance which id was set;
    :param ec2_client: boto3 client connection with ec2 service;
    :param instance_id: instance id for receiving base info.
    """
    reservations = []
    try:
        reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    except ClientError as e:
        print(f"Describe Instances error: {e}")

    base_info = {
        "instance_id": instance_id,
        "instance_type": None,
        "public_ip": None,
        "instance_state": None
    }

    for reservation in reservations:
        for instance in reservation["Instances"]:
            base_info["instance_type"] = instance["InstanceType"]
            base_info["public_ip"] = instance["PublicIpAddress"]
            base_info["instance_state"] = instance["State"]["Name"]

    print(f"Instance info:")
    print(f"\t\tid:\t{base_info['instance_id']}")
    print(f"\t\ttype:\t{base_info['instance_type']}")
    print(f"\t\tpublic ip:\t{base_info['public_ip']}")
    print(f"\t\tstate:\t{base_info['instance_state']}")


def get_running_instances(ec2_client):
    """
    Printing all instances which running in right now on AWS EC2 server;
    :param ec2_client: boto3 client connection with ec2 service;
    """
    reservations = []
    try:
        reservations = ec2_client.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]).get("Reservations")
    except ClientError as e:
        print(f"Describe Instances error: {e}")

    print("Instance Id\t\t|\ttype\t|\tpublic ip\t|\tstate")
    print("============================================")
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            instance_state = instance["State"]["Name"]

            print("{}\t|\t{}\t|\t{}\t|\t{}".format(
                instance_id, instance_type, public_ip, instance_state
            ))


def get_instance_pub_ip(ec2_client, instance_id):
    """
    Printing public ip of instance which id was set;
    :param ec2_client: boto3 client connection with ec2 service;
    :param instance_id: instance id for receiving public IP.
    """
    reservations = []
    try:
        reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    except ClientError as e:
        print(f"Describe Instances error: {e}")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            print("Instance public ip: {}".format(instance.get("PublicIpAddress")))


def get_instance_info(ec2_client, instance_id, info_type=None):
    """
    Grant access to information about EC2 instance;
    :param ec2_client: boto3 client connection with ec2 service;
    :param instance_id: instance id for receiving info about it;
    :param info_type: information type which needs to show;
    """
    match info_type:
        case "base_info": get_instance_base_info(ec2_client, instance_id)
        case "pub_ip": get_instance_pub_ip(ec2_client, instance_id)
        case _: get_running_instances(ec2_client)


def terminate_instance(ec2_client, instance_id):
    """
    Terminate (delete) EC2 instance from AWS EC2 server through boto3 client command;
    Before deleting, instance stopping;
    :param ec2_client: boto3 client connection with ec2 service;
    :param instance_id: instance id which needs to be deleted;
    """
    try:
        # Define running instances list
        reservations = ec2_client.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]).get("Reservations")
        # Stop instance if it's running
        for reservation in reservations:
            for instance in reservation["Instances"]:
                if instance["InstanceId"] == instance_id:
                    ec2_client.stop_instances(InstanceIds=[instance_id])
        # Terminate instance
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Termination instance with id: {instance_id} done successfully!")
    except ClientError as e:
        print(f"Termination instance error: {e}")
