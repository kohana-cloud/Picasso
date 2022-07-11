import botocore
from .aws_session import AWS_Session, ACCESS_KEY



class AWS_S3():

	"""
	Description: These functions aws_s3_{create,stop,destroy,list_all} are used to build start stop and destroy S3 bucket instances in AWS via python function calls.
	Notes:
	"""

	def __init__(self, aws_session):
		self.session = aws_session.session
		self.aws_region_name = aws_session.aws_region_name
		self.account_id = self.session.client('sts').get_caller_identity().get('Account')
		print("AWS_S3[AWS_Session({%s})] bound in region({%s})" % (self.session.profile_name, self.session.region_name))


	def bucket_exist(self, bucket_name):
		s3 = self.session.resource('s3')
		return s3.lookup(bucket_name) is None

	def create(self, bucket_name, s3_region='us-east-1'):
		client = self.session.client('s3', region_name=s3_region)
		try:
			if s3_region != self.aws_region_name:
				response = client.create_bucket(
					#ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
					Bucket=bucket_name,
					CreateBucketConfiguration={
						'LocationConstraint': s3_region # if multiply regions use LocationConstraint: 'EU'|'eu-west-1'
					}
				)
			else:
				response = client.create_bucket(
					Bucket=bucket_name,
				)
			print('AWS_S3[AWS_Session({%s})]:Bucket %s created' % (self.session.profile_name, bucket_name))
			if self.apply_bpa(bucket_name) is None:
				print('AWS_S3[AWS_Session({%s})]: Error could not set BPA for Bucket %s created' % (self.session.profile_name, bucket_name))
				return response

			client.put_bucket_versioning(
				Bucket=bucket_name,
				VersioningConfiguration={
					'Status': 'Enabled'
				},
			)
			print('AWS_S3[AWS_Session({%s})]: Creating versioning for the bucket %s' % (self.session.profile_name, bucket_name))

		except botocore.exceptions.ClientError as e:
			print("unexpected error: %s" % (e.response))
			return None
		return response

	def destroy(self, bucket_name, s3_region=None):
		client = self.session.client('s3', region_name=s3_region)
		try:
			resp = client.delete_bucket(Bucket=bucket_name)
		except botocore.exceptions.ClientError as e:
			print("unexpected error: %s" % (e.response))
			return None
		return resp	

	def list_all(self):
		s3_client = self.session.client('s3')
		response = s3_client.list_buckets()
		return response['Buckets']	

	def apply_bpa(self, bucket_name):
		# Apply secure Blocking Public Access settings to an S3 Storage bucket
		try:
			client = self.session.client('s3')
			response_public = client.put_public_access_block(
				Bucket=bucket_name,
				PublicAccessBlockConfiguration={
					'BlockPublicAcls': True,
					'IgnorePublicAcls': True,
					'BlockPublicPolicy': True,
					'RestrictPublicBuckets': True
				},
				ExpectedBucketOwner= self.account_id
    		)
			print('AWS_S3[AWS_Session({%s})]: Blocking Public Access for the bucket %s' % (self.session.profile_name, bucket_name))
		except client.exceptions.NoSuchBucket:
			print('AWS_S3[AWS_Session({%s})]: bucket %s does not exists' % (self.session.profile_name, bucket_name))
			return None	
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
				print('AWS_S3[AWS_Session({%s})]: account %s does not have a PublicAccessBlockConfiguration set' % (self.session.profile_name, account_id))
			else:
				print("unexpected error: %s" % (e.response))
			return None
		return response_public
		
		
	
	def get_bpa_config(self, bucket_name):
		# Return the Blocking Public Access of an S3 Storage bucket
		try:
			client = self.session.client('s3')
			resp = client.get_public_access_block(
				Bucket=bucket_name,
				ExpectedBucketOwner=self.account_id
			)
		except client.exceptions.NoSuchBucket:
			print('AWS_S3[AWS_Session({%s})]: bucket %s does not exists' % (self.session.profile_name, bucket_name))
			return None
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
				print('AWS_S3[AWS_Session({%s})]: account %s does not have a PublicAccessBlockConfiguration set' % (self.session.profile_name, account_id))
			else:
				print("unexpected error: %s" % (e.response))
			return None
		return resp['PublicAccessBlockConfiguration']
