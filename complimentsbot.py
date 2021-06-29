import time
from telebot import TeleBot
from random import choice, randint
from requests import get
from bs4 import BeautifulSoup
import sqlite3

BOT = TeleBot("TOKEN")
WEBSITE = 'http://kompli.me/komplimenty-devushke'
CONNECT = sqlite3.connect('compliments.db')
CURSOR = CONNECT.cursor()


def send_compliment():
    compliment = get_random_compliment()
    while compliment:
        BOT.send_message("Girlfriend ID", compliment)
        compliment = get_random_compliment()
        sleep = randint(25000, 33000)
        time.sleep(sleep)
    BOT.send_message("Girlfriend ID", "Комплименты кончились")


def get_random_compliment():
    database_create()
    exist = CURSOR.execute('''SELECT * FROM compliments''').fetchall()

    if not exist:
        get_all_compliments()

    compliments = CURSOR.execute('''SELECT * FROM compliments WHERE used = 'No';''').fetchall()
    if not compliments:
        return None

    compliment = choice(compliments)
    compliment_index = int(compliment[0])
    database_update(compliment_index)
    compliment_text = compliment[1]
    return compliment_text


def get_all_compliments():
    tags_of_page_numbers = BeautifulSoup(get(WEBSITE).text, 'html.parser').select('div.nav-links a')
    count_of_page = int(tags_of_page_numbers[-2].text)
    index = 0
    for page in range(1, count_of_page + 1):
        webpage = get(WEBSITE + '/page' + str(page)).text
        tags_of_compliments = BeautifulSoup(webpage, 'html.parser').find_all('div', {"class": "post-card__title"})
        for tag in tags_of_compliments:
            database_append((index, tag.text, 'No'))
            index += 1


def database_create():
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS compliments(
           compliment_id INT PRIMARY KEY,
           compliment TEXT,
           used TEXT);
        ''')
    CONNECT.commit()


def database_append(compliments_tuple):
    CURSOR.execute('''INSERT INTO compliments VALUES(?, ?, ?);''', compliments_tuple)
    CONNECT.commit()


def database_update(compliment_id):
    CURSOR.execute('''UPDATE compliments 
            SET used = 'Yes'
            WHERE compliment_id = (?)''', (compliment_id,))
    CONNECT.commit()


send_compliment()
