# cfleet-ec2-shotty
Python scripts to automate EC2 snapshots using boto3

## About

This is a demo project, using boto3 to manage

AWS EC2 snapshots

## Configuring

shotty uses configuration file created by aws cli e.g.

`aws configure --profile shotty`

## Running
shotty

`pipenv run "python shotty/shotty.py <command> <subcommand> <--project=PROJECT>"`

*Command* is instances, volumes, or snapshots

*Subcommand* - Depends on command

*Project* is optional parameter
