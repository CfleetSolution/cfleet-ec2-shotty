import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


# Defining function to list all instances for your access
@click.command()
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name)))

# Best practice to call function in main body of the script
if __name__ == '__main__':
    list_instances()
