import api
from random import random
from time import sleep

def get_photos(photo_list):
	photos = []

	for photo in photo_list:
		photos.append(photo['url'])
	
	return photos

def rate(photos):
	print(photos)
	r = random()
	return r

while True:
	recom = api.get_recommendations()
	profiles = recom['results']

	for profile in profiles:
		profile = profile['user']
		# print(profile)
		photos = get_photos(profile['photos'])
		rating = rate(photos)

		if rating > 0.5:
			api.like(profile['_id'])
			print("Liked:", profile['_id'])
		else:
			api.dislike(profile['_id'])
			print("Disliked:", profile['_id'])

		sleep(5)


# while True:
# 	try:
# 		self.swipe_right
# 	except Exception:
# 		try:
# 			self.close_match()
# 		except Exception:
# 			self.close_popup()

# 	sleep(1)





# from selenium import webdriver
# from time import sleep

# from secret import email, password

# class TinderBot():
# 	def __init__(self):
# 		# options = webdriver.ChromeOptions()
# 		# options.add_argument('headless')
# 		self.driver = webdriver.Chrome(executable_path="C:/Developer/chromedriver.exe") #, chrome_options=options)

# 	def login(self):
# 		# go to Tinder.com
# 		self.driver.get('https://tinder.com')

# 		sleep(10)

# 		# select the facebook login button and click it
# 		fb_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
# 		fb_button.click()

# 		sleep(10)

# 		# save main window and login popup window
# 		main_window = self.driver.window_handles[0]
# 		login_window = self.driver.window_handles[1]
# 		# switch windows
# 		self.driver.switch_to_window(login_window)

# 		# # get email and pass
# 		# f = open("secret.txt", "r")
# 		# e = f.readline().strip()
# 		# p = f.readline().strip()
# 		# f.close()

# 		# write email and password then click login
# 		email_field = self.driver.find_element_by_xpath('//*[@id="email"]')
# 		email_field.send_keys(email)

# 		pass_field = self.driver.find_element_by_xpath('//*[@id="pass"]')
# 		pass_field.send_keys(password)

# 		login_button = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
# 		login_button.click()

# 		# switch windows again
# 		self.driver.switch_to_window(main_window)
		
# 		#close popups
# 		popup1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
# 		popup1.click()

# 		popup2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
# 		popup2.click()

# 		popup3 = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/button')
# 		popup3.click()
	
# 	def swipe_right(self):
# 		like_button = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]')
# 		like_button.click()
# 		sleep(5)

# 	def swipe_left(self):
# 		dislike_button = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
# 		dislike_button.click()
# 		sleep(5)
	
# 	def close_match(self):
# 		keep_swiping = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
# 		keep_swiping.click()


# 	def close_popup(self):
# 		print("nothing to do")
	
# 	def auto_swipe(self):
# 		while True:
# 			try:
# 				self.swipe_right
# 			except Exception:
# 				try:
# 					self.close_match()
# 				except Exception:
# 					self.close_popup()

# 			sleep(1)
		
# bot = TinderBot()

# bot.login()

# bot.auto_swipe()



