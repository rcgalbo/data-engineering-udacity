import argparse
import configparser
import boto3


def create_bucket(bucket_name, session, region='us-west-2'):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-west-2).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        s3_client = session.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read('dl.cfg')
    
    key = config['AWS']['AWS_ACCESS_KEY_ID']
    secret = config['AWS']['AWS_SECRET_ACCESS_KEY']

    session = boto3.Session(key, secret)
    
    parser = argparse.ArgumentParser(description='Create S3 bucket')
    parser.add_argument('name', type=str, help='a name for the bucket')
    args = parser.parse_args()
    
    assert create_bucket(args.name, session) != False