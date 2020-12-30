import telebot
from telebot import types
from utils import *

from secret_config import *

bot = telebot.TeleBot(BOT_TOKEN)


requestsWrapper = RequetsWrapper()