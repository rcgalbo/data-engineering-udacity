import json
import configparser
import boto3

from create_cluster import create_session


def delete_cluster(session, config):
    """Delete's redshift cluster
    session: boto3 session object
    config: ConfigParser object
    returns: None
    """
    DWH_CLUSTER_IDENTIFIER = config['CLUSTER']['DWH_CLUSTER_IDENTIFIER']
    redshift = session.client('redshift')
    redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
    
def delete_iam(session, config):
    """Delete cluster IAM role
    
    """
    iam = session.client('iam')
    DWH_IAM_ROLE_NAME = config['CLUSTER']['DWH_IAM_ROLE_NAME']
    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    
if __name__ == "__main__":
    
    print('----    loading configuration    ----')    
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))
    
    print('----    creating session    ----')
    session = create_session(config['AWS']['KEY'], config['AWS']['SECRET'])

    print('----    deleting cluster    ----')
    delete_cluster(session, config)
    
    print('----    deleting IAM role    ----')
    delete_iam(session, config)