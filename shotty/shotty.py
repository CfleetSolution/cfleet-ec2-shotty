import boto3
import botocore
import click

# Retriving session info from the profile created through AWS-CLI
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

def has_snapshot_in_progress(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

# Grouping mulitiple operations of EC2 instances
@click.group()
def cli():
    """ Shotty manages snapshots """

# Grouping snapshots operation
@cli.group('snapshots')
def snapshots():
    """ Commands for snapshots """

# Grouping volumes operation
@cli.group('volumes')
def volumes():
    """ Commands for volumes """

# Grouping instances operation
@cli.group('instances')
def instances():
    """ Commands for instances """

# Creating snapshots operation
@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")
@click.option('--all','list_all', default=False, is_flag=True,
    help='List all snapshot for all volumes not just the recent one')

# Function definition for Listing EC2 volumes snapshots
def list_snapshots(project, list_all):
    "List EC2 volumes snapshots"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
                for s in v.snapshots.all():
                    print(", ".join((
                        s.id,
                        v.id,
                        i.id,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c")
                        )))

                    if s.state == 'completed' and not list_all: break
    return

# Creating volumes operation
@volumes.command('list')
@click.option('--project', default=None,
    help="Only volumes for project (tag Project:<name>)")

# Function definition for Listing EC2 volumes
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

# Creating instances operation
@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Function definition for Listing EC2 instances
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
    return

@instances.command('snapshot', help="Creating Snapshots of all volumes")
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")

# Function definition for creating snapshot of EC2 instances
def create_snapshots(project):
    "Create EC2 snapshots of all volumes"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping instance {0}..".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_snapshot_in_progress(v):
                print (" Skipping snapshot of volume {0}, already in progress".format(v.id))
                continue

            print(" Creating snapshot of {0}...".format(v.id))
            v.create_snapshot(Description = "Created by Cfleet SnapshotsAlyzer!")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    print("Job's done!")
    return

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Function definition for stopping EC2 instances
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print ("Couldn't stop {0}. ".format(i.id) + str(e))
            continue

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# Function definition for starting EC2 instances
def start_instances(project):
    "Start EC2 intances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Couldn't start intance {0}. ".format(i.id) + str(e))
            continue

    return

# Best practice to call function in main body of the script
if __name__ == '__main__':
    cli()
