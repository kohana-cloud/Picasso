import botocore
import logging
from .aws_session import AWS_Session, ACCESS_KEY

logger = logging.getLogger(__name__)


class AWS_SQS():

	"""
	Description: These functions aws_sqs_{create,stop,destroy,list_all} are used to build start stop and destroy a Amazon Simple Queuing Service instances in AWS via python function calls.
	Notes: Amazon Simple Queuing Service (Amazon SQS) is a distributed messaging system that helps you to send, store, and receive messages between web services and software components at 
		any scale without losing messages or requiring services or application components to be available all the time.
	"""

	def __init__(self, aws_session):
		self.session = aws_session.session
		self.aws_region_name = aws_session.aws_region_name
		self.account_id = self.session.client('sts').get_caller_identity().get('Account')
		print("AWS_SQS[AWS_Session({%s})] bound in region({%s})" % (self.session.profile_name, self.session.region_name))	


	def create(self, queue_name, s3_region='us-east-1', delay_seconds='0', visiblity_timeout='60'):
		client = self.session.resource('sqs', region_name=s3_region)

		try:
			response = client.create_queue(QueueName=queue_name,
                                             Attributes={
                                                 'DelaySeconds': delay_seconds,
                                                 'VisibilityTimeout': visiblity_timeout
                                             })
			logger.info(
       			f'SQS Standard Queue {queue_name} created. Queue URL - {response.url}')
		except botocore.exceptions.ClientError as e:
			logger.exception(f'Could not create SQS queue - {queue_name}.')
			print("unexpected error: %s" % (e.response))
			return None
		return response