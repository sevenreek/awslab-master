import configure
import boto3
from configure import *
from concurrent.futures import ProcessPoolExecutor, Future
from multiprocessing import Semaphore
import json
from image_processors import *
from time import sleep
import os
from traceback import print_exc


def process_message(message_body):
    print("Processing message")
    processing_methods = {
        Thumbnailer.NAME : Thumbnailer(),
        ImageInverter.NAME : ImageInverter(),
    }
    try:
        rq = json.loads(message_body)
        filename = rq['filename']
        method = rq['process']
        destination = rq.get('destination', filename)
    except:
        print("Failed to parse message")
        print_exc()
        return
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET_NAME)
    except:
        print("Worker failed to obtain bucket")
        print_exc()
        return
    try:
        print(f"Downloading {filename}")
        bucket.download_file(filename, os.path.join(SCRIPT_ROOT_DIRECTORY,filename))
    except:
        print("Requested file could not be downloaded")
        print_exc()
        return
    try:
        print(f"Processing {os.path.join(SCRIPT_ROOT_DIRECTORY, filename)}->{os.path.join(SCRIPT_ROOT_DIRECTORY,destination)}")
        processing_methods[method](os.path.join(SCRIPT_ROOT_DIRECTORY, filename), os.path.join(SCRIPT_ROOT_DIRECTORY,destination))
        thumb_filename = os.path.join(SCRIPT_ROOT_DIRECTORY,'thumb_' + destination)
        processing_methods['thumbnail'](os.path.join(SCRIPT_ROOT_DIRECTORY, destination), thumb_filename)
    except:
        print("Requested file could not be processed")
        print_exc()
        return
    try:
        print(f"Uploading {os.path.join(SCRIPT_ROOT_DIRECTORY, destination)}->{destination}")
        bucket.upload_file(os.path.join(SCRIPT_ROOT_DIRECTORY, destination), destination, ExtraArgs={'ACL':'public-read'})
        bucket.upload_file(thumb_filename, THUMBS_DIR+'/'+destination, ExtraArgs={'ACL':'public-read'})

    except:
        print("Requested file could not be uploaded")
        print_exc()
        return
    print(f"Processed image {filename}")


if __name__ == '__main__':
    app = AWSApplication()
    print("Using queue: ",app.queue.url)

    active = True
    POOL_SIZE = max(CPU_COUNT-1, 1)
    print("Pool size is ", POOL_SIZE)
    available_workers = Semaphore(POOL_SIZE)
    def on_worker_done(future):
        available_workers.release()
    
    with ProcessPoolExecutor(max_workers=POOL_SIZE) as process_pool:
        while(active):
            try:
                messages = app.queue.receive_messages(MaxNumberOfMessages=available_workers.get_value())
                for message in messages:
                    print(message.body)
                    try:
                        print("Creating worker")
                        available_workers.acquire()
                        fut = process_pool.submit(process_message, message.body)
                        fut.add_done_callback(on_worker_done)
                    except:
                        print("Could not process message in pool.\n", message)
                        continue
                    
                    # Let the queue know that the message is processed
                    message.delete()

                if(len(messages) == 0):
                    sleep(NO_MESSAGES_SLEEP_TIME)
                    print("No messages. Sleeping...")
            except KeyboardInterrupt:
                active = False
                break
            
        print("Shutting down...")
    #cleanup_all()