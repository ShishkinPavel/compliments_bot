from telebot import TeleBot
from random import randint, choice
from requests import get
from bs4 import BeautifulSoup
from threading import Timer

BOT = TeleBot("BOT_TOKEN")


def send_compliment():
    Timer(28800.0, send_compliment).start()
    BOT.send_message("Girlfriend_id", get_random_compliment())


def get_random_compliment():
    random_page_number = str(randint(1, 42))
    webpage = get('http://kompli.me/komplimenty-devushke/page/' + random_page_number).text
    tags = BeautifulSoup(webpage, 'html.parser').find_all('a')
    compliments = []
    for tag in tags:
        tag_text = tag.get_text()
        if tag_text == 'Назад':
            break
        compliments.append(tag_text)

    return choice(compliments[4:])


send_compliment()
