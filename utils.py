from instabot import *
import pickle 
from secret_config import *
import numpy as np


class RequetsWrapper:
	def __init__(self):
		self.bot = Bot()
		self.bot.login(username = INST_USERNAME,  password = INST_PASSWORD)

	def get_media_info(self, media_link):
		media_pk = self.bot.get_media_id_from_link(media_link)
		media_info = self.bot.get_media_info(media_pk)
		if (media_info != None):
			return media_info[0]
		else:
			return None

	def get_profile_info(self, username):
		user_info = self.bot.get_user_info(username)
		return user_info

	def amount_of_comments(self, media_link):
		media_pk = self.bot.get_media_id_from_link(media_link)
		media_info = self.bot.get_media_info(media_pk)[0]
		comment_count = media_info["comment_count"]
		return comment_count

	def amount_of_followers(self, username):
		user_info = self.bot.get_user_info(username)
		if (user_info == None):
			return None
		return user_info["follower_count"] 

	def amount_of_likers(self, media_link):
		media_pk = self.bot.get_media_id_from_link(media_link)
		media_info = self.bot.get_media_info(media_pk)[0]
		like_count = media_info["like_count"]
		return like_count

	def get_followers_for(self, username):
		user_followers = self.bot.get_user_followers(username)
		return user_followers

	def users_liked(self, media_link):
		try:
			media_pk = self.bot.get_media_id_from_link(media_link)
			users_liked = self.bot.get_media_likers(media_pk)
			return users_liked
		except:
			return None

	def choose_N_random_followers(self, username, N):
		user_followers = self.get_followers_for(username)
		if (user_followers == None):
			return None
		winners_indices = np.random.choice(len(user_followers), N, replace=False)
		winners_usernames = [self.bot.get_username_from_user_id(user_followers[i]) for i in winners_indices]
		return winners_usernames

	def choose_N_random_likers(self, media_link, N):
		users_liked = self.users_liked(media_link)
		if (users_liked == None):
			return None
		winners_indices = np.random.choice(len(users_liked), N, replace=False)
		winners_usernames = [self.bot.get_username_from_user_id(users_liked[i]) for i in winners_indices]
		return winners_usernames

	def choose_N_random_commentators(self, media_link, N):
		media_pk = self.bot.get_media_id_from_link(media_link)
		all_comments = self.bot.get_media_comments_all(media_pk)
		users_commented = set()
		for comment in all_comments:
			users_commented.add(comment["user"]["username"])

		if (users_commented == set()):
			return None

		users_commented = list(users_commented)
		winners_indices = np.random.choice(len(users_commented), N, replace=False)
		winners_usernames = [users_commented[i] for i in winners_indices]
		return winners_usernames

	

	def users_commented(self, media_link):
		try:
			media_id = self.bot.get_media_id_from_link(media_link)
			users_commented = self.bot.get_media_commenters(media_id)
			return users_commented
		except:
			return None

	def get_common_followers(self, username_1, username_2):
		user_followers_1 = self.get_followers_for(username_1)
		user_followers_2 = self.get_followers_for(username_2)

		if ((user_followers_1 == None) or (user_followers_2 == None)):
			return None
		common_followers = list(set(user_followers_1) & set(user_followers_2))
		if (len(common_followers) > 100):
			return None

		common_followers_usernames = [self.bot.get_username_from_user_id(user_id) for user_id in common_followers]
		return common_followers_usernames

class AllUsers:
	def __init__(self):
		self.all_users = {}
		self.__refresh_database__()

	def __refresh_database__(self):
		try:
			with open('all_users.pkl', 'rb') as f:
				self.all_users = pickle.load(f)
		except:
			pass

	def __save_database__(self):
		with open('all_users.pkl', 'wb') as f:
			pickle.dump(self.all_users, f)

	def add_user(self, user):
		userID = user.id
		self.all_users[userID] = user
		self.__save_database__()
