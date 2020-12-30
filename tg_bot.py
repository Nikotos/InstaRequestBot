from bot_config import *
import json

def send_file_to_user(chat_id, file_path):
	with open(file_path, "rb") as file_to_send:
		bot.send_document(chat_id, file_to_send)

def save_json_to_file(data, file_path):
	with open(file_path, "w") as f:
		json.dump(data, f)
	return file_path

def error_handler(chat_id, error_key):
	if (error_key == "incorrect_input_format"):
		bot.send_message(chat_id, "Неверный формат использования комманды")
	elif(error_key == "request_out_of_bounds"):
		bot.send_message(chat_id, "Такой запрос не может быть выполнен")
	elif(error_key == "invalid_account"):
		bot.send_message(chat_id, "Нет доступа к такому аккаунту. Либо он не существует, либо имеет статус закрытого")
	elif(error_key == "too_many_followers"):
		bot.send_message(chat_id, "Слишком много подписчкиков")
	elif(error_key == "invalid_post"):
		bot.send_message(chat_id, "Пост недоступен")
	elif(error_key == "too_many_commetns"):
		bot.send_message(chat_id, "Слишком много комментариев")
	elif(error_key == "too_many_likes"):
		bot.send_message(chat_id, "Слишком много лайков")
	elif(error_key == "error_common_followers"):
		bot.send_message(chat_id, "Либо одного из аккаунтов не существует, либло превышен лимит запроса")
	elif(error_key == "no_comments"):
		bot.send_message(chat_id, "Под указанным постом нет комментариев")
	elif(error_key == "no_likes"):
		bot.send_message(chat_id, "Под указанным постом нет лайков")



def say_hello_at_the_very_begining(chat_id):
	keyboard = types.InlineKeyboardMarkup() 

	hooray = types.InlineKeyboardButton(text='Инструкция', callback_data='get_instruction') 
	keyboard.add(hooray)

	with open("texts/hooray.txt", "r") as file:
		contents = file.read()

	bot.send_message(chat_id, text=contents, reply_markup=keyboard) 


def send_instruction(chat_id):
	keyboard = types.InlineKeyboardMarkup() 

	with open("texts/instruction.txt", "r") as file:
		contents = file.read()

	bot.send_message(chat_id, text=contents, parse_mode="markdown") 



@bot.callback_query_handler(func=lambda call: True) 
def callback_query_handler(call):
	if(call.data == "get_instruction"):
		send_instruction(call.message.chat.id)

@bot.message_handler(commands=["start"]) 
def initial_hooray(message): 
	# allUsers.add_user(message.from_user)
	say_hello_at_the_very_begining(message.chat.id)

@bot.message_handler(commands=["help"]) 
def initial_hooray(message): 
	say_hello_at_the_very_begining(message.chat.id)

# duplicatre for simplier call
@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/1 " in message.text)) 
def choose_n_random_followers_1(message): 
	choose_n_random_followers(message)

@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/choose_n_random_followers" in message.text)) 
def choose_n_random_followers(message): 
	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 3):
		error_handler(chat_id, "incorrect_input_format")
		return None

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	username = data[2]

	amount_of_followers = requestsWrapper.amount_of_followers(username)

	if(amount_of_followers == None):
		error_handler(chat_id, "invalid_account")
		return None
	if(amount_of_followers == 0):
		error_handler(chat_id, "invalid_account")
		return None
	elif (amount_of_followers > 10000):
		error_handler(chat_id, "too_many_followers")
		return None

	try:
		N = int(data[1])
		if ((N > 20) or (N < 1)):
			error_handler(chat_id, "request_out_of_bounds")
			return None
	except:
		error_handler(chat_id, "incorrect_input_format")
		return None

	winners = requestsWrapper.choose_N_random_followers(username, N)
	result = ""
	for name in winners:
		result += name + "\n"

	bot.send_message(chat_id, result)


@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/2 " in message.text)) 
def choose_n_random_likers_1(message): 
	choose_n_random_likers(message)

# here N does straight after command!
@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/choose_n_random_likers" in message.text)) 
def choose_n_random_likers(message): 

	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 3):
		error_handler(chat_id, "incorrect_input_format")
		return None

	try:
		N = int(data[1])
		if (N > 20):
			error_handler(chat_id, "request_out_of_bounds")
			return None
	except:
		error_handler(chat_id, "incorrect_input_format")
		return None


	media_link = data[2]

	amount_of_likers = requestsWrapper.amount_of_likers(media_link)

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	if(amount_of_likers == None):
		error_handler(chat_id, "invalid_post")
		return None
	elif(amount_of_likers == 0):
		error_handler(chat_id, "no_likes")
		return None
	elif (amount_of_likers > 1000):
		error_handler(chat_id, "too_many_likes")
		return None

	winners = requestsWrapper.choose_N_random_likers(media_link, N)
	result = ""
	for name in winners:
		result += name + "\n"

	bot.send_message(chat_id, result)


@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/3 " in message.text)) 
def choose_n_random_commentators_1(message): 
	choose_n_random_commentators(message)

# here N does straight after command!
@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/choose_n_random_commentators" in message.text)) 
def choose_n_random_commentators(message): 

	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 3):
		error_handler(chat_id, "incorrect_input_format")
		return None

	try:
		N = int(data[1])
		if (N > 20):
			error_handler(chat_id, "request_out_of_bounds")
			return None
	except:
		error_handler(chat_id, "incorrect_input_format")
		return None


	media_link = data[2]

	amount_of_comments = requestsWrapper.amount_of_comments(media_link)

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	if(amount_of_comments == None):
		error_handler(chat_id, "invalid_post")
		return None
	elif(amount_of_comments == 0):
		error_handler(chat_id, "no_comments")
		return None
	elif (amount_of_comments > 1000):
		error_handler(chat_id, "too_many_comments")
		return None

	winners = requestsWrapper.choose_N_random_commentators(media_link, N)
	result = ""
	for name in winners:
		result += name + "\n"


	bot.send_message(chat_id, result)


@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/4 " in message.text)) 
def common_followers_1(message): 
	common_followers(message)

@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/common_followers" in message.text)) 
def common_followers(message): 
	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 3):
		error_handler(chat_id, "incorrect_input_format")
		return None

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	username_1 = data[1]

	amount_of_followers_1 = requestsWrapper.amount_of_followers(username_1)

	if(amount_of_followers_1 == None):
		error_handler(chat_id, "invalid_account")
		return None
	elif (amount_of_followers_1 > 10000):
		error_handler(chat_id, "too_many_followers")
		return None

	username_2 = data[2]
	amount_of_followers_2 = requestsWrapper.amount_of_followers(username_1)

	if(amount_of_followers_2 == None):
		error_handler(chat_id, "invalid_account")
		return None
	elif (amount_of_followers_2 > 10000):
		error_handler(chat_id, "too_many_followers")
		return None

	common_followers = requestsWrapper.get_common_followers(username_1, username_2)

	if (common_followers == None):
		error_handler(chat_id, "error_common_followers")
		return None

	result = ""
	for name in common_followers:
		result += name + "\n"

	if (result == ""):
		result = "Общих подписчиков нет, либо один из аккаунтов закрытый"

	bot.send_message(chat_id, result)


@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/5 " in message.text)) 
def get_profile_info_1(message): 
	get_profile_info(message)

@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/get_profile_info" in message.text)) 
def get_profile_info(message): 
	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 2):
		error_handler(chat_id, "incorrect_input_format")
		return None

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	username = data[1]

	user_info = requestsWrapper.get_profile_info(username)

	if (user_info == None):
		error_handler(chat_id, "invalid_account")
		return None

	file_path = "data/user_info_" + str(chat_id) + ".json"
	save_json_to_file(user_info, file_path)
	send_file_to_user(chat_id, file_path)


@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/6 " in message.text)) 
def get_media_info_1(message): 
	get_media_info(message)

@bot.message_handler(content_types=["text"], func=lambda message: (message.text != None) and ("/get_media_info" in message.text)) 
def get_media_info(message): 
	chat_id = message.chat.id
	data = message.text.split(" ")

	if (len(data) != 2):
		error_handler(chat_id, "incorrect_input_format")
		return None

	bot.send_message(chat_id, "запрос принят, обрабатывается, это может занять некоторое время")

	media_link = data[1]

	media_info = requestsWrapper.get_media_info(media_link)

	if (media_info == None):
		error_handler(chat_id, "invalid_post")
		return None

	file_path = "data/media_info_" + str(chat_id) + ".json"
	save_json_to_file(media_info, file_path)
	send_file_to_user(chat_id, file_path)


if __name__ == "__main__":
	bot.polling(none_stop=True, interval=0)


