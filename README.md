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

`pipenv run "python shotty/shotty.py <command> <--project=PROJECT>"`

*Command* is list, start, stop
*Project* is optional 
