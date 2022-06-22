import docker
import os
import base64
from .aws_session import AWS_Session

class AWS_ECR():
	def __init__(self, aws_session):
		self.session = aws_session.session
		print("AWS_ECR[AWS_Session({%s})] bound in region({%s})" % (self.session.profile_name, self.session.region_name))

	"""
	Description: These functions aws_ecs_{create,start,stop,destroy} are used to build start stop and destroy ECS instances in AWS via python function calls.

	Parameters:
	- instance_identifier: this is a uuid that represents the instance, i would like to make it a 12-15 digit alphanumeric value, but if you have constraints let me know
	- image_uri: this is a string that points to the ECR URI where we are storing the honeypot docker images

	Return:
	- response_status: boolean status indicator of success/failure. An integer would be acceptable as well if the response is not discrete.
	"""

	def aws_ecr_delete(self, repo_name:str, image_tag:str):
		client = self.session.client('ecr')
		all_repos = self.aws_ecr_list_repo()
		ecr_repo = next((x for x in all_repos if x['repositoryName'] == repo_name), None)
		if not ecr_repo:
			print("Error: the repo does not exist")
			return False

		batch_delete_response = client.batch_delete_image(
			repositoryName=repo_name,
			imageIds=[{"imageTag": image_tag}],
		)

		if batch_delete_response["failures"] and len(batch_delete_response["failures"]):
			print("Error: Failed to call ecr batch-delete-image")
			#TODO LOG error stack trace
			print(batch_delete_response)
			return False

		print("AWS_ECR[AWS_Session({%s})] successfully delete image {%s}:{%s}" % (self.session.profile_name, repo_name, image_tag))
		return True

	def aws_ecr_update(self, repo_name:str, image_tag='latest'):
		#TODO
		return True

	def aws_ecr_add(self, repo_name:str, local_image_name:str, image_tag='latest'):
		client = self.session.client('ecr')
		all_repos = self.aws_ecr_list_repo()
		ecr_repo = next((x for x in all_repos if x['repositoryName'] == repo_name), None)

		if not ecr_repo:
			ecr_repo = client.create_repository(
				repositoryName=repo_name, encryptionConfiguration={"encryptionType": "KMS"}
			)["repository"]
			print("AWS_Session({%s}): created repo %s" % (self.session.profile_name, ecr_repo['repositoryUri']))
		

		# get local docker client
		docker_client = docker.from_env()
		#build/tag image here....
		LOCAL_REPOSITORY = repo_name
		image, build_log = docker_client.images.build(path=(os.path.join(os.getcwd(), 'images', local_image_name)), tag=LOCAL_REPOSITORY, rm=True)
		# then override the docker client config by passing auth_config
		# pass an auth_config with username/password when pushing the image to ECR.
		ecr_credentials = (
			client
			.get_authorization_token()
			['authorizationData'][0])
		ecr_username = 'AWS'
		ecr_password = (
			base64.b64decode(ecr_credentials['authorizationToken'])
			.replace(b'AWS:', b'')
			.decode('utf-8'))
		ecr_url = ecr_credentials['proxyEndpoint']
		# get Docker to login/authenticate with ECR
		docker_client.login(
        	username=ecr_username, password=ecr_password, registry=ecr_url)
		# tag image for AWS ECR
		ecr_repo_name = '{}/{}'.format(
			ecr_url.replace('https://', ''), LOCAL_REPOSITORY)
		image.tag(ecr_repo_name, tag=image_tag)

		# push image to AWS ECR
		push_log = docker_client.images.push(ecr_repo_name, tag=image_tag)
		print(push_log)
	

		return True

	def aws_ecr_list_repo(self):
		client = self.session.client('ecr')
		resp = client.describe_repositories()['repositories']
		return resp
		