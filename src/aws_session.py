import boto3
import os
import base64
import docker
from botocore.config import Config
from .aws_query import AWS_LIST_RESOURCE_QUERIES, run_raw_operation

ACCESS_KEY="XXXX"
SECRET_KEY="XXXX"

SERVICE_BLACKLIST= ['alexaforbusiness', 'kinesis-video-media']

class AWS_Session():
	def __init__(self):
		#See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#guide-credentials for more details
		self.aws_region_name = os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1' 
		self.session = boto3.Session(
				aws_access_key_id=ACCESS_KEY,
				aws_secret_access_key=SECRET_KEY,
				region_name=self.aws_region_name,
		)
		
		print("AWS_Session({%s}) bound in region({%s})" % (self.session.profile_name, self.session.region_name))

	def get_services_names(self):
		"""Return a list of available service names e.g. 's3' or 'ec2'."""
		return [service for service in sorted(self.session.get_available_services()) if service not in SERVICE_BLACKLIST]

	def get_region_list(self):
		print("* Getting region names", flush=True)
		EC2_REGIONS = set([region['RegionName'] for region in self.session.client("ec2").describe_regions()['Regions']])
		S3_REGIONS = set(self.session.get_available_regions('s3'))
		ALL_REGIONS = sorted(EC2_REGIONS | S3_REGIONS)
		return ALL_REGIONS

	def get_regional_sessions_using_root_user(self):
		ALL_REGIONS = self.get_region_list()
		print("* Initializating %d regional session" % len(ALL_REGIONS))
		sessions = {region: boto3.Session(
			aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY,
			region_name=region,
			) for region in ALL_REGIONS
		}
		if sessions[ALL_REGIONS[0]].get_credentials() is None:
			print("WARNING: No credentials available for listing. ")
		return sessions

	def get_regional_sessions(self, credentials):
		ALL_REGIONS = self.get_region_list()
		print("* Initializating %d regional session" % len(ALL_REGIONS))
		sessions = {region: boto3.Session(
			aws_access_key_id=credentials['AccessKeyId'],
			aws_secret_access_key=credentials['SecretAccessKey'],
			aws_session_token=credentials['SessionToken'],
			region_name=region,
			) for region in ALL_REGIONS
		}
		if sessions[ALL_REGIONS[0]].get_credentials() is None:
			print("WARNING: No credentials available for listing. ")
		return sessions	

	#FIXME
	def get_sts_role_credentials(self): 
		sts_client = boto3.client('sts', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
		assumed_role_object=sts_client.assume_role(
			RoleArn="arn:aws:iam::032622136258:role/KohanaAdmin",
			RoleSessionName="AssumeRoleSession1"
		)
		credentials=assumed_role_object['Credentials']
		print(credentials)
		return credentials

	
	def get_all_services(self):
		all_services = self.get_services_names()
		sts_credentials = self.get_sts_role_credentials()
		regional_sessions = self.get_regional_sessions(sts_credentials)
		result = {}


		for service in all_services:
			method_to_call = AWS_LIST_RESOURCE_QUERIES.get(service) #TODO: snakecase
			if method_to_call is None:
				continue
			result[service] = {}
			for region, session in regional_sessions.items():
				if region == 'ap-east-1':
					continue
				handler = session.client(
					service,
					#endpoint_url="https://sts.{}.amazonaws.com".format(region),
					config=Config(
						retries={
							"max_attempts": 10,
							'mode': 'standard'
						}
					),
				)
				print("Enabling (%s,%s)" % (service, region))
				result[service][region] = run_raw_operation(handler, method_to_call)
				
		return result


	def get_resources_taggingapi(self, region="us-west-1"):
		tagapi = self.session.client('resourcegroupstaggingapi', region_name=region)
		resp = tagapi.get_resources(ResourcesPerPage=2)
		for resource in resp['ResourceTagMappingList']:
			print("Resource: ", resource)
		return resp

	def get_all_rds_instances(self):
		return self.session.client('rds').describe_db_instances()

	def get_all_buckets(self):
		s3 = self.session.resource('s3')
		return s3.buckets.all()

	def aws_ecr_add(self, repo_name, image_name):
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
		image, build_log = docker_client.images.build(path=("./images/{}".format(image_name)), tag=LOCAL_REPOSITORY, rm=True)
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
		image.tag(ecr_repo_name, tag='latest')

		# push image to AWS ECR
		push_log = docker_client.images.push(ecr_repo_name, tag='latest')
		print(push_log)
	

		return True

	def aws_ecr_list_repo(self):
		client = self.session.client('ecr')
		resp = client.describe_repositories()['repositories']
		return resp
		


