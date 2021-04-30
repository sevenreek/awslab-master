import os
import multiprocessing
import boto3
from dotenv import load_dotenv
from traceback import print_exc
load_dotenv()

AWS_ACCESS_KEY=os.getenv('aws_access_key_id')
AWS_SECRET_ACCESS_KEY=os.getenv('aws_secret_access_key')
AWS_SESSION_TOKEN=os.getenv('aws_session_token')
AWS_DEFAULT_REGION=os.getenv('aws_default_region')


CPU_COUNT = multiprocessing.cpu_count()

QUEUE_NAME = os.getenv('aws_queue_name')
QUEUE_ATTRIBUTES = {
    'DelaySeconds': '0',
    'ReceiveMessageWaitTimeSeconds': str(20),
    'VisibilityTimeout': str(60)
}

NO_MESSAGES_SLEEP_TIME = 20
WORKERS_BUSY_SLEEP_TIME = 3

BUCKET_NAME = os.getenv('aws_bucket_name')
BUCKET_ACL = 'public-read'
THUMBS_DIR = 'thumbs'

SCRIPT_ROOT_DIRECTORY = (os.path.dirname(os.path.realpath(__file__)))

class AWSApplication():
    def __init__(self):
        # Get or create SQS
        self.sqs = boto3.resource('sqs', 
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_DEFAULT_REGION
        )

        # Get the queue. This returns an SQS.Queue instance
        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        except:
        # Create the queue. This returns an SQS.Queue instance
            print_exc()
            print("Queue does not exist")
            exit(1)

        # Get or create S3
        self.s3 = boto3.resource('s3', 
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_DEFAULT_REGION
        )
        self.bucket = self.s3.Bucket(BUCKET_NAME)
        self.bucket.load()
        if(self.bucket.creation_date is None):
            print("Bucket does not exist")
            exit(1)


