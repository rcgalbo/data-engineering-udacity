import json
import configparser
import boto3


def create_session(key, secret, region='us-west-2'):
    """Creates boto3 session
    key: aws api key
    secret: aws api secret
    region: aws region for session
    returns: boto3 session object
    """
    session = boto3.Session(region_name=region,
                        aws_access_key_id=key,
                        aws_secret_access_key=secret)
    return session

def create_iam_role(session, config):
    """Creates IAM role for Redshift cluster and returns role ARN
    session: boto3 session object
    configuration: ConfigParser object
    returns: None
    """
    DWH_IAM_ROLE_NAME = config['CLUSTER']['DWH_IAM_ROLE_NAME']
    
    iam = session.client('iam')
    dwhRole = iam.create_role(
        Path='/',
        RoleName=DWH_IAM_ROLE_NAME,
        Description='Allows Redshift clusters to call AWS services on your behalf.',
        AssumeRolePolicyDocument=json.dumps(
            {'Statement': [{'Action': 'sts:AssumeRole',
                           'Effect': 'Allow',
                           'Principal': {'Service': 'redshift.amazonaws.com'}}],
            'Version': '2012-10-17'}
        )        
    )
    status = iam.attach_role_policy(
                    RoleName=DWH_IAM_ROLE_NAME,
                    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                )['ResponseMetadata']['HTTPStatusCode']
    assert status == 200

def fetch_arn(session, config):
    """Get ARN from specified IAM role 
    session: boto3 session object
    configuration: ConfigParser obejct
    returns: ARN
    """
    DWH_IAM_ROLE_NAME = config['CLUSTER']['DWH_IAM_ROLE_NAME']
    iam = session.client('iam')

    return iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']



def create_cluster(session, config, role_arn):
    """Create a redshif cluster with specified IAM role 
    session: boto3 session object
    configuration: ConfigParser object
    role_arn: IAM role arn
    returns: None
    """
    
    DWH_CLUSTER_TYPE = config["CLUSTER"]["DWH_CLUSTER_TYPE"]
    DWH_NODE_TYPE = config["CLUSTER"]["DWH_NODE_TYPE"]
    DWH_NUM_NODES = config["CLUSTER"]["DWH_NUM_NODES"]
    DWH_DB = config["CLUSTER"]["DWH_DB"]
    DWH_CLUSTER_IDENTIFIER = config["CLUSTER"]["DWH_CLUSTER_IDENTIFIER"]
    DWH_DB_USER = config["CLUSTER"]["DWH_DB_USER"]
    DWH_DB_PASSWORD = config["CLUSTER"]["DWH_DB_PASSWORD"]
    DWH_PORT = config["CLUSTER"]["DWH_PORT"]
    
    redshift = session.client('redshift')
    
    try:
        response = redshift.create_cluster(        
            ClusterType = DWH_CLUSTER_TYPE,
            NodeType = DWH_NODE_TYPE,
            NumberOfNodes = int(DWH_NUM_NODES),
            DBName = DWH_DB,
            ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,
            MasterUsername = DWH_DB_USER,
            MasterUserPassword = DWH_DB_PASSWORD,
            IamRoles = [role_arn]
        )
    except Exception as e:
        print(e)
        
def open_port(session, config):
    """Opens port on the VPC security group for connection
    session: boto3 session object
    config: ConfigParser object
    return: None
    """
    
    ec2 = session.resource('ec2')
    redshift = session.client('redshift')
    
    DWH_CLUSTER_IDENTIFIER = config['CLUSTER']['DWH_CLUSTER_IDENTIFIER']
    DWH_PORT = config['CLUSTER']['DWH_PORT']
    
    vpc_id = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]['VpcId']
    try:
        vpc = ec2.Vpc(id=vpc_id)
        defaultSg = list(vpc.security_groups.all())[0]

        defaultSg.authorize_ingress(
            GroupName= defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        print(e)    

def check_cluster_status(session, config):
    """Get cluster status
    session: boto3 session object
    config: ConfigParser object
    return: string status of redshift cluster
    """
    DWH_CLUSTER_IDENTIFIER = config['CLUSTER']['DWH_CLUSTER_IDENTIFIER']
    redshift = session.client('redshift')
    cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    cluster_status = cluster_props['ClusterStatus']
    return cluster_status.lower()

def get_cluster_endpoint(session, config):
    """Get cluster endpoint
    session: boto3 session object
    config: ConfigParser object
    return: string for cluster endpoint
    """
    DWH_CLUSTER_IDENTIFIER = config['CLUSTER']['DWH_CLUSTER_IDENTIFIER']
    redshift = session.client('redshift')
    cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    return cluster_props['Endpoint']['Address']

    

def get_connection_str(session, config):
    """Get connection string from running cluster
    session: boto3 session object
    config: ConfigParser object
    return: postgresql flavor connection string
    """
    
    DWH_DB_USER = config["CLUSTER"]["DWH_DB_USER"]
    DWH_DB_PASSWORD = config["CLUSTER"]["DWH_DB_PASSWORD"]
    DWH_PORT = config["CLUSTER"]["DWH_PORT"]
    DWH_DB = config["CLUSTER"]["DWH_DB"]
    
    try: 
        assert check_cluster_status(session, config) == 'available'
        DWH_ENDPOINT = get_cluster_endpoint(session, config)
        con_str = f"postgresql://{DWH_DB_USER}:{DWH_DB_PASSWORD}@{DWH_ENDPOINT}:{DWH_PORT}/{DWH_DB}"
        return con_str
    except Exception as e:
        print(e)
        print('Cluster not yet available')
        return None
    
    
if __name__ == '__main__':
    print('----    loading configuration    ----')    
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))
    
    print('----    creating session    ----')
    session = create_session(config['AWS']['KEY'], config['AWS']['SECRET'])
    
    print('----    creating IAM role    ----')
    try:
        create_iam_role(session, config)
    except Exception as e:
        print(e)
    print('----    fetching ARN    ----')
    role_arn = fetch_arn(session, config)
    
    print('----    creating redshift cluster    ----')
    create_cluster(session, config, role_arn)
    
    print('----    open port    ----')
    open_port(session, config)