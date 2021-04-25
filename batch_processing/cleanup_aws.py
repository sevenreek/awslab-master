import configure
from configure import *

def delete_bucket():
    # delete bucket
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()

def delete_queue():
    # delete sqs
    queue.delete()

def cleanup_all():
    delete_bucket()
    delete_queue()

if __name__ == '__main__':
    cleanup_all()