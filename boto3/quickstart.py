import configure

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)


# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
try:
    queue = sqs.get_queue_by_name(QueueName='test')
except:
# Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

# Create a new message
response = queue.send_message(MessageBody='world')

# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))

for message in queue.receive_messages(MaxNumberOfMessages=10):
    # Get the custom author message attribute if it was set
    # Print out the body and author (if set)
    print('Hello, {0}!'.format(message.body))

    # Let the queue know that the message is processed
    message.delete()