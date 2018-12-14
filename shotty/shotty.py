import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

# Helper function to filter intances by project name
def filter_instances(project):
    "Filter intances by project"
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

# Grouping mulitiple operations for instances
@click.group()
def instances():
    """ Commands for instances """

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Funtion definition for Listing EC2 instances
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Funtion definition for stopping EC2 instances
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Funtion definition for starting EC2 instances
def start_instances(project):
    "Start EC2 intances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return
 
# Best practice to call function in main body of the script
if __name__ == '__main__':
    instances()
