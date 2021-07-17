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


# input_photos = ['https://images-ssl.gotinder.com/u/othWwJgb9HQoHnxiVCxH2S/xx6A1PTDcMgUB6eardtoSm.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9vdGhXd0pnYjlIUW9IbnhpVkN4SDJTLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=c9GT8uoi38Ljy6mAUmNa6UV9omW3-gF0RUsyAkNmmNVp6X7S-E~4lW2si4l3e~6GmsGPzQYoW3CkPgqbQt6gFU4yufXiJEo3ZneVVa0-Idj~CukhfpBHTtA4EZU~YpLcofWezkP2HIWApkEXI-p3OaKgH1I9mTwiB-4Va-tYZXwFnPse5NKHkPUZq4rEaTD1LLo4jn2DZy5guW5xctXl8JfrDoq6WZ4CuWuTh00drirOwEPGoLx82~55ZViCJquaU6KWu2~wMD4a40GMUFzT1ZSkWVCeKy-A4pThTDeYKrmtXb2tFIBx1MBxCi5Cmnk~bQgVXl2AlGnPw8g-39lIew__&Key-Pair-Id=K368TLDEUPA6OI', 'https://images-ssl.gotinder.com/u/bRuTv2sTByE8YXYaU5wx5Y/72moipfRtwnfKSMmCiQEi5.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9iUnVUdjJzVEJ5RThZWFlhVTV3eDVZLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=w5uFzUC1Ze9u8CREdfXNwJi5K8Fu~VDs5vy9-ikRKdg1ZpyfT2Z8Pxe~EZURu-NOzki5YK8BUZobFVY1iPkJiZeOT9t9HRW0rjAtxgM6x0ZtBtBxMr-ShfIh6iLSxNtliWppIjzNXrKuM8SKaaQ~DYdw4tMCLys1npTNb~eb7IN95IQM5PB-Y0cSCfh1DGTfjQ2t~2QP7BsCBTDXh4Nrc3sI50orN9kblIUly5nj~0r2tzXgqwkHE8uv7ntDYTEwELddmb0DD5oHlVOByJgPKjLmRie7B3RRieZjkaZ7eVDir2J0-KTM9tj2cDEzCS6-IfNWaymFo7LG0JXjtRvZ3g__&Key-Pair-Id=K368TLDEUPA6OI', 'https://images-ssl.gotinder.com/u/b6VN6tL5iCuQ83UZZiz2ME/9usxJWzABCn5gaSDdbe7CV.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9iNlZONnRMNWlDdVE4M1VaWml6Mk1FLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=AF9RzzpafKZueXads2BevAIcRM9VMfuNi4wRba8yaodmVGCrN2Y42~EH09YYLWacdIago4c4~iM5P0d4ylCVv8ESu2nucakIOED4vH~9ed1rO751WV1PR7lfrUwQa5Iqr8N9np0kLxrsdUqp9qc1btJpOhgkhXFQhfRyflElISDscJ0WOxqtrwOUtHJXJWvyhLrFCHMpDYQ7QKSiJjtcqUjLN82D9Ptz83lTci9vBqZn0AUpXcq~Ksab1waxsokVusWVyRQMMTUWueJ-LrU5TKJPTb6XWh0Igtl1hBRVafT46nyaqPLbJ3nIiDu0LCk9tbaVIhJQbG-EYpc8I6o99A__&Key-Pair-Id=K368TLDEUPA6OI', 'https://images-ssl.gotinder.com/u/8YCcb8regGkqt8hC1KhM6t/4G8bjSaBaePUehRsrByTxC.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS84WUNjYjhyZWdHa3F0OGhDMUtoTTZ0LyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=QvFHWs8zIJC~n4YycMmRHqnCbfcjyUA-zeJ1BSWaFV1xjqg9Z7i13yFIxpOh9ucCF-K-vxBgqMrEiTAuqVvBpb93~zIsW9ez95aAeJeK8UYsoVciXMa9jND5ipFUpGwIR1vI7q6v0bejytfY114q668W~nqVsPKWO8mtati1X7XKYnJ8qM0aZ7fR-aQ-bfQXaKNVUHSkD~ljRq07YR59vd2PMW2zlsTNaw7zY15WtqNXWrilB9QDpHmnt451D44AfsZJWkSUkmr-eTQpb54gZAgY6-cOS6u40sqxNPoceHfv4we80ra-66yELLmh-nU9yH6J~I6e6BhM5t1vcPqh7g__&Key-Pair-Id=K368TLDEUPA6OI', 'https://images-ssl.gotinder.com/u/iENWw4eBuyxopKGRH5NCyW/wBYxcgAPjnTGV77KmFKXU7.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9pRU5XdzRlQnV5eG9wS0dSSDVOQ3lXLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=B-iJdjB1jrL0GMOiRSc9ajEDnflNf~ENRhotWIO2kSHpU9WUOcIbhaS-w1ggU2q8F~1MUa7xZVIRmXiJo5tceFS8dXDSZv7yugaOLS6SHCzqCYXceVz38u7i9o00JZC8~zyy2UPngeBJzyEI17~S-8o2SwZij~S4OzE9vBVQ8JD-TrCb1leaNCsm8auFd~F~Ywx9QaMSpC6u6TPYdlJNS8tHHQAcXmLBc7g94J7cDLJmAKpiAI7VsUCd8dtuFuo4taj4MoOXZJ87pvk8iOlcuufAeVzZVdIh76QPkRLU70T31FK~zZOUYHx4yipYdiMb5rCORtlVV0QQY7M8CKVDaA__&Key-Pair-Id=K368TLDEUPA6OI', 'https://images-ssl.gotinder.com/u/potryEAtpr7xRGo6mrtu3N/mzRVda2TfE2fC9kJsJ1qdE.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9wb3RyeUVBdHByN3hSR282bXJ0dTNOLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MjY3NjE3NDZ9fX1dfQ__&Signature=ZwkpxS1VD~SbQc4bh9dhvhxRHIvjnT-b7Rr0MCqIpV1IXLYVbt9lWdRTjo501xYXPWN6mOfw7kCg1llRftCNA5wqYXi-yHMAJG0QJncv-BZc8BBpcCzFZTKMgFm9JdGJMguIXtAcBJRpsV4cnWECOd-HI79mdeElOvSxHhjXG-Dv8tPOZrFhXqYA1pFrpZb9uaXWCF474jifVtH9fqTDabb0WHPCYe1WylKemrE4SUvUbWvlxfNbA3Y0N4WHw6c1CN978iSHfJ0aLVgzFp12hP1fMW9hXWwVVmgrwpth6GxSiMVs06mJHH4Y1B1loKHqeUzLaM15TKVkxYlMJdAQyg__&Key-Pair-Id=K368TLDEUPA6OI']

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

if __name__ == "__main__":
	rating = get_face_rating(input_photos)
	print(rating)
