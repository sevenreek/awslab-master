import configure
import json
from configure import *
from image_processor.image_processors import ImageInverter

#bucket.upload_file(os.path.join(SCRIPT_ROOT_DIRECTORY, 'lenna.png'), 'lenna.png')

mbody = {
    'filename':'lenna.png',
    'destination':'invert_lenna.png',
    'process': ImageInverter.NAME
}
queue.send_message(MessageBody=json.dumps(mbody))