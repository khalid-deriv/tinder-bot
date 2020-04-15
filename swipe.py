import api
from random import random
from time import sleep

def get_photos(photo_list):
	photos = []

	for photo in photo_list:
		photos.append(photo['url'])
	
	return photos

def rate(photos):
	r = random()
	return r

while True:
	recom = api.get_recommendations()
	profiles = recom['results']

	for profile in profiles:
		profile = profile['user']
		photos = get_photos(profile['photos'])
		rating = rate(photos)

		if rating > 0.5:
			api.like(profile['_id'])
			print("Liked:", profile['_id'])
		else:
			api.dislike(profile['_id'])
			print("Disliked:", profile['_id'])

		sleep(5)

