import docker
import os
import botocore
import json
import time
from .aws_session import AWS_Session, ACCESS_KEY


LINUX_ECS_HVM_GP2_AMI = 'ami-0f863d7367abe5d6f'
EC2_ECS_ACCESS_ROLE = 'ecsInstanceRole'
EC2_ECS_INST_PROFILE_NAME = 'ecsInstanceRole-instance-profile'

class AWS_ECS():
	def __init__(self, aws_session):
		self.session = aws_session.session
		self.account_id = self.session.client('sts').get_caller_identity().get('Account')
		print("AWS_ECS[AWS_Session({%s})] bound in region({%s})" % (self.session.profile_name, self.session.region_name))

	"""
	Description: These functions aws_ecs_{create,start,stop,destroy} are used to build start stop and destroy ECS instances in AWS via python function calls.
	Notes:
	- An Amazon ECS cluster is a logical grouping of tasks or services. Your tasks and services are run on infrastructure that is registered to a cluster.
	- An Amazon ECS task is the blueprint describing which Docker containers to run and represents your application. It includes several tasks.
	- An Amazon ECS service is an instance of Task Definition. It also defines the minimum and maximum Tasks from one Task Definition run at any given time, autoscaling, and load balancing.

	Parameters:
	- instance_identifier: this is a uuid that represents the instance, i would like to make it a 12-15 digit alphanumeric value, but if you have constraints let me know
	- image_uri: this is a string that points to the ECR URI where we are storing the honeypot docker images

	Return:
	- response_status: boolean status indicator of success/failure. An integer would be acceptable as well if the response is not discrete.
	"""
	def create_key_pair(self, name):
		ec2_client = self.session.client('ec2')
		resp = ec2_client.describe_key_pairs()['KeyPairs']
		key_entry = next((x for x in resp if x['KeyName'] == name), None)
		if key_entry != None:
			return
		
		resp = ec2_client.create_key_pair(KeyName=name)

		key_file_path = 'registry%s%s.pem' % (os.sep, name)
		private_key_file=open(key_file_path,"w")
		private_key_file.write(resp['KeyMaterial'])
		private_key_file.close()

		print('AWS_EC2[AWS_Session({%s})]: created keypair %s' % (self.session.profile_name, key_file_path))

	def create_instance_profile(self, inst_profile_name, add_role_to_instance_name):
		iam = self.session.client('iam')
		try:
			instance_profile = iam.create_instance_profile (
				InstanceProfileName = inst_profile_name
			)
			print('AWS_IAM[AWS_Session({%s})]: created InstanceProfileName %s' % (self.session.profile_name, inst_profile_name))
			
			response = iam.add_role_to_instance_profile (
				InstanceProfileName = inst_profile_name,
				RoleName            = add_role_to_instance_name 
			)
			print('AWS_IAM[AWS_Session({%s})]: Added InstanceProfileName %s to Role %s' % (self.session.profile_name, inst_profile_name, add_role_to_instance_name))
			
			# Sleep 2 seconds for AWS to synchronize
			time.sleep(2)
		except iam.exceptions.EntityAlreadyExistsException:
			print('AWS_IAM[AWS_Session({%s})]: InstanceProfileName %s already exists' % (self.session.profile_name, inst_profile_name))
		except botocore.exceptions.ParamValidationError as e:
			print("AWS_IAM[AWS_Session({%s})]: Parameter validation error: %s" % (self.session.profile_name, e))
			return False
		return True

	def create_ec2_ecs_role(self, role_name):
		assume_role_policy_document = json.dumps({
			"Version": "2008-10-17",
			"Statement": [
				{
				"Effect": "Allow",
				"Principal": {
					"Service": "ec2.amazonaws.com"
				},
				"Action": "sts:AssumeRole"
				}
			]
		})
		try:
			iam = self.session.client('iam')
			create_role_response = iam.create_role(
				RoleName = role_name,
				Description = 'Allows EC2 instances in an ECS cluster to access ECS.',
				AssumeRolePolicyDocument = assume_role_policy_document,
				Tags=[
					{
						'Key': 'KOHANA-DECOY-FAMILY',
						'Value': 'K-001'
					},
				],
			)['Role']
			#print(create_role_response['Arn'])

			attach_policy_reponse = iam.attach_role_policy(
				PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role',
				RoleName=role_name
			)
		except iam.exceptions.EntityAlreadyExistsException:
			print('AWS_IAM[AWS_Session({%s})]: Role %s already exists' % (self.session.profile_name, role_name))
		except botocore.exceptions.ParamValidationError as e:
			print("AWS_IAM[AWS_Session({%s})]: Parameter validation error: %s" % (self.session.profile_name, e))
			return False
		#TODO return false on catching any other error
		
		return True

	def aws_ecs_create(self, cluster_name:str, instance_identifier:str, image_uri:str, service_name:str, task_name:str):
		ecr_cluster_arn = "arn:aws:ecs:{}:{}:cluster/{}".format(self.session.region_name, self.account_id, cluster_name)
		inst_profile_name = EC2_ECS_INST_PROFILE_NAME
		inst_profile_arn = "arn:aws:iam::{}:instance-profile/{}".format(self.account_id, inst_profile_name)

		# List all ECS clusters	
		client = self.session.client('ecs')
		all_clusters = self.aws_ecs_list_clusters()

		# Create the ECS cluster if it does not already exist 
		if ecr_cluster_arn not in all_clusters:
			ecr_cluster = client.create_cluster(
				clusterName=cluster_name,
        		settings=[{"name": "containerInsights", "value": "disabled"}],
			)["cluster"]
			print("AWS_ECS[AWS_Session({%s})]: created cluster %s" % (self.session.profile_name, ecr_cluster['clusterArn']))

			# Create IAM ecsInstanceRole role
			if not self.create_ec2_ecs_role(EC2_ECS_ACCESS_ROLE):
				print("AWS_ECS[AWS_Session({%s})]: Error to create IAM ECS-EC2 role %s" % (self.session.profile_name, EC2_ECS_ACCESS_ROLE))
				return False

			# Attach instance profile to ecsInstanceRole role
			if not self.create_instance_profile(inst_profile_name, EC2_ECS_ACCESS_ROLE):
				print("AWS_ECS[AWS_Session({%s})]: Error to Attach instance profile %s to ecsInstanceRole role" % (self.session.profile_name, inst_profile_name))
				return False

			# Create an SSH keypair that will be sequentely associated to the EC2
			self.create_key_pair(cluster_name)

			# Create EC2 instance(s) in the cluster
			# For now I expect a default cluster to be there
			ec2_client = self.session.client('ec2')
			

			# By default, your container instance launches into your default cluster.
			# If you want to launch into your own cluster instead of the default,
			# choose the Advanced Details list and paste the following script
			# into the User data field, replacing your_cluster_name with the name of your cluster.
			# !/bin/bash
			# echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config

			response = ec2_client.run_instances(
				# Use the official ECS image
				ImageId=LINUX_ECS_HVM_GP2_AMI,
				KeyName=cluster_name,
				MinCount=1,
				MaxCount=1,
				InstanceType="t2.micro",
				UserData="#!/bin/bash \n yum update -y \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config",
				IamInstanceProfile={
					'Arn': inst_profile_arn,
				},
				TagSpecifications=[
					{
						'ResourceType': 'instance',
						'Tags': [
							{
								'Key': 'KOHANA-DECOY-FAMILY',
								'Value': 'K-001'
							}
						]
					}
				]		
			)

			#TODO save the instance ID in storage
			ec2_instance_id = response['Instances'][0]['InstanceId']
			print('AWS_EC2[AWS_Session({%s})]: created EC2 instance %s' % (self.session.profile_name, ec2_instance_id))

		
		taskdef = client.register_task_definition(
			family=task_name, 			#Task definition name
			containerDefinitions=[
				{
					"name": task_name,  #CONTAINER_NAME
					"image": image_uri, #DOCKER_IMAGE
					"cpu": 1,
					"memory": 400,
					"essential": True,
					"mountPoints": [],
					"volumesFrom": [],
					"portMappings": [
						{
							'containerPort': 8888,
							'hostPort': 8888,
							'protocol': 'tcp'
						},
					],
					"environment": [
						{"name": "AWS_ACCESS_KEY_ID", "value": ACCESS_KEY}
					],
					"logConfiguration": {"logDriver": "json-file"},
				}
			],
			requiresCompatibilities=[
				"EC2"
			],
			networkMode="bridge"
		)["taskDefinition"]

		if len(taskdef['containerDefinitions']):
			print('AWS_ECS[AWS_Session({%s})]: created task_definition %s' % (self.session.profile_name, taskdef['taskDefinitionArn']))
			
		taskdef_aws_name = taskdef['taskDefinitionArn'].split("/")[1]

		#TODO update service if it exists and Try/catch
		resp = client.create_service(
			cluster=cluster_name,
			serviceName=service_name,
			taskDefinition=taskdef_aws_name,
			desiredCount=1,
			#networkConfiguration={
			#	'awsvpcConfiguration': {
			#		'subnets': ['xxxxxxxxxxx'],
			#		'securityGroups': ["xxxxxxxxxxxxx"]
			#	}
			#},
			tags=[
				{
					'key': 'KOHANA-DECOY-FAMILY',
					'value': 'K-001'
				},
			],			
			#clientToken='request_identifier_string',
			deploymentConfiguration={
				'maximumPercent': 200,
				'minimumHealthyPercent': 50
			},
			launchType='EC2'
		)["service"]
		
		if resp["launchType"] == 'EC2':
			print('AWS_ECS[AWS_Session({%s})]: created service %s' % (self.session.profile_name, resp['serviceArn']))
		else:
			print('AWS_ECS[AWS_Session({%s})]: failed to create service %s' % (self.session.profile_name, service_name))
			return False
			

		return True

	def aws_ecs_start(self, instance_identifier:str, image_uri:str):
		#TODO
		return True	

	def aws_ecs_stop(self, instance_identifier:str, image_uri:str):
		#TODO
		return True	

	def aws_ecs_destroy(self, instance_identifier:str, image_uri:str):
		#TODO
		return True

	def aws_ecs_list_clusters(self):
		client = self.session.client('ecs')
		resp = client.list_clusters()['clusterArns']
		return resp

	def aws_ecs_delete_cluster(self, cluster_name:str):
		client = self.session.client('ecs')
		resp = client.delete_cluster(cluster=cluster_name)
		if resp and resp["cluster"]["clusterName"]:
			print("AWS_ECS[AWS_Session({%s})]: deleted cluster %s" % (self.session.profile_name, cluster_name))
			return True
		return False