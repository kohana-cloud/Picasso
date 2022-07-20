import logging
from ..sqs._long_polling import AWSLongPollSQSListener

logger = logging.getLogger(__name__)

class AWSS3EventListener(AWSLongPollSQSListener):

	def parseMessage(self, message):
		#print("Parsing ", message)
		if 'Records' in message:
			for record in message['Records']:
				match record['eventName']:
					case 'ObjectCreated.CompleteMultipartUpload' | 'ObjectCreated:Post' | 'ObjectCreated:Copy' | 'ObjectCreated:Put':
						print("AWSS3EventListener: [{}] Object {} has been added".format(record['s3']['bucket']['name'], record['s3']['object']['key']))
					case 'ObjectRemoved:DeleteMarkerCreated' | 'ObjectRemoved:Delete':
						print("AWSS3EventListener: [{}] Object {} has been deleted".format(record['s3']['bucket']['name'], record['s3']['object']['key']))
					case _:
						logger.error('S3 Event {} not recognized '.format(record['eventName']))