# Importing libraries for interaction with AWS
from botocore.exceptions import ClientError
# Importing standard libraries
import os

# Import utils for load config
from attrdict import AttrDict
from src.utils import load_config

CONFIG = AttrDict(load_config())


def create_bucket(s3_client, bucket_name):
    """"""
    try:
        location = {"LocationConstraint": CONFIG.boto.region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(f"Creation bucket error: {e}")
        return False
    print(f"Bucket '{bucket_name}' was create successfully!")
    return True


def upload_file(s3_client, bucket_name, file_path, bucket_file_name=None):
    """
    Upload a file to on S3 bucket;
    :param s3_client: client for manipulating with S3 Bucket;
    :param bucket_name: Bucket to upload to;
    :param file_path: file to upload;
    :param bucket_file_name: S3 object name (if not specified then file_name is used);
    :return: True if file was uploaded, else False.
    """
    # If s3 bucket file name was not specified, use file_name with 's3_' in begin of the file name
    if bucket_file_name is None:
        bucket_file_name = "s3_" + os.path.basename(file_path)

    # Upload the file
    try:
        s3_client.upload_file(file_path, bucket_name, bucket_file_name)
    except ClientError as e:
        print(f"Upload file error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    return True


def download_file(s3_client, bucket_name, bucket_file_name, file_path=None):
    """
    Download a file from S3 bucket;
    :param s3_client: client for manipulating with S3 Bucket;
    :param bucket_name: Bucket download from;
    :param bucket_file_name: S3 object name (if not specified then file_path is used);
    :param file_path: file path to download;
    :return: True if file was downloaded, else False.
    """
    # If file_name was not specified, use file_name
    if file_path is None:
        file_path = "../output/" + os.path.basename(bucket_file_name)

    # Download the file
    try:
        s3_client.download_file(bucket_name, bucket_file_name, file_path)
    except ClientError as e:
        print(f"Download file error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    return True


def bucket_manipulation(s3_client, bucket_name, action=None, file_path=None, bucket_file=None):
    """"""
    match action:
        case "upload": upload_file(s3_client, bucket_name, file_path, bucket_file)
        case "download": download_file(s3_client, bucket_name, bucket_file, file_path)
        case _: print("Please choose available actions [upload|download].")


def get_existing_buckets(s3_client):
    """"""
    response = s3_client.list_buckets()

    # Output the bucket names list
    print("Existing buckets in your region:")
    for bucket in response["Buckets"]:
        print(f"\t{bucket['Name']}")


def get_files_in_bucket(s3_client, bucket_name=None):
    """"""
    contents = []
    if bucket_name is None:
        print("Please enter bucket name!!")
    try:
        contents = s3_client.list_objects(Bucket=bucket_name, MaxKeys=10).get("Contents")
    except ClientError as e:
        print(f"Get Files object error: {e}")

    print("List of object in bucket:")
    for bucket_obj in contents:
        print(f"File: {bucket_obj['Key']}")
        print(f"Storage Class: {bucket_obj['StorageClass']}")
        print("---------------------------")


def get_bucket_info(s3_client, bucket_name=None, info_type="list"):
    """"""
    match info_type:
        case "list": get_existing_buckets(s3_client)
        case "files": get_files_in_bucket(s3_client, bucket_name)
        case _: print("Please choose available info type [list|files].")


def delete_bucket(s3_client, bucket_name):
    """"""
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        print(f"Deletion bucket error: {e}")
        return False
    print(f"Bucket '{bucket_name}' was delete successfully!")
    return True
