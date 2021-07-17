import numpy as np
import cv2
from tensorflow import keras
import face_recognition
from statistics import mean
from urllib.request import urlopen
import os
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)


rating_model = keras.models.load_model("rating_model.h5")
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def get_photos(photo_list):
	photos = []

	for photo in photo_list:

		url_response = urlopen(photo['url'])
		img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
		img = cv2.imdecode(img_array, -1)
		photos.append(img)
	
	return photos

def get_face_rating(input_photos):
	photos = get_photos(input_photos)
	rating_list = []
	error_images = []
	for i in range(len(photos)):
		try:
			photo = photos[i]
			# detect MultiScale / faces
			faces = classifier.detectMultiScale(photo)

			# get the first face only
			face = faces[0]

			(x, y, w, h) = face
			sub_face = photo[y:y+h, x:x+w]

			face_encoding = face_recognition.face_encodings(sub_face)[0]

			x = np.asarray(face_encoding.tolist()).astype("float32").reshape((1, 128))
			x = x.tolist()

			prediction = rating_model.predict(x)
			rating_list.append(float(prediction)*2)
		except:
			error_images.append(i)

	if (len(rating_list) > 1): return mean(rating_list)
	elif (len(rating_list) == 1): return rating_list[0]
	else: return 0

