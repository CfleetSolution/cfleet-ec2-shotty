import boto3

# Listing EC2 instances available in my environment
if __name__ == '__main__':
    session = boto3.Session(profile_name='shotty')
    ec2 = session.resource('ec2')

    for i in ec2.instances.all():
        print(i)
