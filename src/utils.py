import boto3
import yaml
from attrdict import AttrDict

CONFIG_PATH = "../config.yaml"


def load_config():
    """"""
    try:
        with open(CONFIG_PATH, 'r') as conf_file:
            config = yaml.safe_load(conf_file)
    except Exception as e:
        print(f"Error reading the config file!: {e}")

    return config


CONFIG = AttrDict(load_config())


def connect_to_boto_client(client_type="ec2"):
    """"""
    client = None
    match client_type:
        case "ec2": client = boto3.client("ec2", region_name=CONFIG.boto.region)
        case "s3": client = boto3.client("s3", region_name=CONFIG.boto.region)
        case _: print("Please choose available client type [ec2|s3]")

    return client
