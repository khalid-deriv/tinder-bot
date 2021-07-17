import api
import rating
from random import random
from time import sleep

threshold = 5

while True:
	recom = api.get_recommendations()
	print("Recommendations:", len(recom))
	profiles = recom['results']

	for profile in profiles:
		profile = profile['user']
		face_rating = rating.get_face_rating(profile['photos'])

		if face_rating > threshold:
			api.like(profile['_id'])
			print("Prodile ID:", profile['_id'])
			print("Rating:", face_rating)
			print("Like!")
		else:
			api.dislike(profile['_id'])
			print("Prodile ID:", profile['_id'])
			print("Rating:", face_rating)
			print("Dislike!")

		sleep(5)

