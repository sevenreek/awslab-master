import os
import multiprocessing
import boto3
from dotenv import load_dotenv
load_dotenv()

CPU_COUNT = multiprocessing.cpu_count()

QUEUE_NAME = os.getenv('AWS_QUEUE_NAME')
QUEUE_ATTRIBUTES = {
    'DelaySeconds': '0',
    'ReceiveMessageWaitTimeSeconds': str(20),
    'VisibilityTimeout': str(60)
}

NO_MESSAGES_SLEEP_TIME = 20

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
BUCKET_ACL = 'public-read'
THUMBS_DIR = 'thumbs'

SCRIPT_ROOT_DIRECTORY = (os.path.dirname(os.path.realpath(__file__)))

class AWSApplication():
    def __init__(self):
        # Get or create SQS
        self.sqs = boto3.resource('sqs')

        # Get the queue. This returns an SQS.Queue instance
        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        except:
        # Create the queue. This returns an SQS.Queue instance
            print("Queue does not exist")
            exit(1)

        # Get or create S3
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(BUCKET_NAME)
        self.bucket.load()
        if(self.bucket.creation_date is None):
            print("Bucket does not exist")
            exit(1)


