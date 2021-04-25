import os
import multiprocessing
import boto3
from dotenv import load_dotenv
load_dotenv()
CPU_COUNT = multiprocessing.cpu_count()

QUEUE_NAME = "217715-psoir-image-queue"
QUEUE_ATTRIBUTES = {
    'DelaySeconds': '0',
    'ReceiveMessageWaitTimeSeconds': str(20),
    'VisibilityTimeout': str(60)
}

NO_MESSAGES_SLEEP_TIME = 20

BUCKET_NAME = "217715-psoir-image-bucket"
BUCKET_ACL = 'public-read'
THUMBS_DIR = 'thumbs'

SCRIPT_ROOT_DIRECTORY = (os.path.dirname(os.path.realpath(__file__)))

# Get or create SQS
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
try:
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
except:
# Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName=QUEUE_NAME, Attributes=QUEUE_ATTRIBUTES)

# Get or create S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
bucket.load()
if(bucket.creation_date is None):
    print("Bucket not found. Creating")
    bucket.create(ACL=BUCKET_ACL)
