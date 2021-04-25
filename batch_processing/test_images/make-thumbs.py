from PIL import Image
import os
for filename in os.listdir('..'):
	if filename.endswith('.jpg') or filename.endswith('.png'):
		image = Image.open(os.path.join('..',filename))
		MAX_SIZE = (128, 128)
		  
		image.thumbnail(MAX_SIZE)
		  
		# creating thumbnail
		image.save(filename)
