from threading import Thread, get_ident
import logging
import boto3
import json
import time
from abc import ABCMeta, abstractmethod
from ..aws_session import AWS_Session, ACCESS_KEY

logger = logging.getLogger(__name__)

SQS_LISTENER_WAIT_IN_TIME_SEC = 5 #20
SQS_LISTENER_MAX_NUMBER_OF_MSG = 1
SQS_POLL_INTERVAL_SEC = 5

class AWSLongPollSQSListener(Thread):
	__metaclass__ = ABCMeta

	def __init__(self, aws_session, queue_name, region_name, msgParsingcallBack=None, queue_acct_id=None):
		Thread.__init__(self, name=queue_name)
		self.session = aws_session.session
		self.region_name = region_name
		self.queue_name = queue_name
		self.queue_acct_id = queue_acct_id
		self.poll_interval = SQS_POLL_INTERVAL_SEC
		sqs_client = aws_session.session.resource('sqs', region_name=region_name)

		if self.queue_acct_id is not None:
			self.queue = sqs_client.get_queue_by_name(QueueName=self.queue_name, QueueOwnerAWSAccountId=self.queue_acct_id)
		else:
			self.queue = sqs_client.get_queue_by_name(QueueName=self.queue_name)
		
		logger.debug('Starting up thread {} and long-polling inbound queue {}'.format(
            get_ident(), self.queue_name
        ))
	
	def run(self):
		logger.debug('AWSLongPollSQSListener {}:{} started'.format(self.region_name, self.queue_name))
		while True:
			messages = self.queue.receive_messages(MaxNumberOfMessages=SQS_LISTENER_MAX_NUMBER_OF_MSG, WaitTimeSeconds=SQS_LISTENER_WAIT_IN_TIME_SEC)
			if len(messages):
				message = messages[0]
				message_attribs = message.message_attributes
				body = message.body
				
				try:
					msg_params_dict = json.loads(body)
				except:
					logger.warning("Unable to parse message - JSON is not formatted properly")
					continue
					
				try:
					self.parseMessage(msg_params_dict)
					logger.debug('AWSLongPollSQSListener {}:{} processed message'.format(self.region_name, self.queue_name))
					message.delete()
				except Exception as ex:
					logger.exception(ex)
			else:
				time.sleep(self.poll_interval)

	@abstractmethod
	def parseMessage(self, message):
		pass
	
	def stop(self):
		logger.debug('AWSLongPollSQSListener {}:{} stopped'.format(self.region_name, self.queue_name))


