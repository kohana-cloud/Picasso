import docker
from .aws_session import AWS_Session

class AWS_ECS():
	def __init__(self, aws_session):
		self.session = aws_session.session
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
	https://gist.github.com/spandanb/cd023a79f0efbd00f929c14aa28ce5b2
	https://github.com/spulec/moto/blob/master/tests/test_ecs/test_ecs_boto3.py
	https://github.com/awslabs/ecr-cleanup-lambda/blob/79614634719dad6e0d97d1c48d00c448cea6784e/main.py#L161
	"""

	def aws_ecs_create(self, cluster_name:str, instance_identifier:str, image_uri:str):
		client = self.session.client('ecs')
		all_clusters = self.aws_ecs_list_clusters()
		ecr_cluster = next((x for x in all_clusters if x['clusterName'] == cluster_name), None)
		if not ecr_cluster:
			ecr_cluster = client.create_cluster(
				clusterName=cluster_name,
        		settings=[{"name": "containerInsights", "value": "disabled"}],
			)["cluster"]
			print(ecr_cluster)
			print("AWS_ECS[AWS_Session({%s})]: created cluster %s" % (self.session.profile_name, ecr_cluster['clusterName']))
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
		resp = client.describe_clusters()['clusters']
		return resp

	def aws_ecs_delete_cluster(self, cluster_name:str):
		client = self.session.client('ecs')
		resp = client.delete_cluster(cluster=cluster_name)
		if resp and resp["cluster"]["clusterName"]:
			print("AWS_ECS[AWS_Session({%s})]: deleted cluster %s" % (self.session.profile_name, cluster_name))
			return True
		return False