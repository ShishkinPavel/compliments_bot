from telebot import TeleBot
from random import randint, choice
from requests import get
from bs4 import BeautifulSoup
from threading import Timer

BOT = TeleBot("BOT_TOKEN")
WEBSITE = 'http://kompli.me/komplimenty-devushke'

def send_compliment():
    Timer(28800.0, send_compliment).start()
    BOT.send_message("Girlfriend_id", get_random_compliment())


def get_random_compliment():
    tags_of_page_numbers = BeautifulSoup(get(WEBSITE).text, 'html.parser').select('div.nav-links a')
    count_of_page = tags_of_page_numbers[-2].text
    random_page_number = str(randint(1, int(count_of_page)))
    webpage = get(WEBSITE + '/page'+ random_page_number).text
    tags_of_compliments = BeautifulSoup(webpage, 'html.parser').find_all('div', {"class": "post-card__title"})
    compliments = [tag.text for tag in tags_of_compliments]
    return choice(compliments)


send_compliment()
