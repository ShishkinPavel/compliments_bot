import random
import time

from telebot import TeleBot
from random import choice
from requests import get
from bs4 import BeautifulSoup
import sqlite3

BOT = TeleBot("TOKEN")
WEBSITE = 'http://kompli.me/komplimenty-devushke'
CONNECT = sqlite3.connect('compliments.db')
CURSOR = CONNECT.cursor()


def send_compliment():
    compliment = get_random_compliment()
    while compliment is not None:
        BOT.send_message("Girlfriend ID", compliment)
        compliment = get_random_compliment()
        sleep = random.randint(20000, 30000)
        time.sleep(sleep)


def get_random_compliment():
    database_create()
    exist = CURSOR.execute('''SELECT * FROM compliments''').fetchall()
    if not exist:
        tags_of_page_numbers = BeautifulSoup(get(WEBSITE).text, 'html.parser').select('div.nav-links a')
        count_of_page = int(tags_of_page_numbers[-2].text)
        xx = get_all_compliments(count_of_page)
        database_append(xx)
    compliments = CURSOR.execute('''SELECT * FROM compliments WHERE used = 'No';''').fetchall()
    if not compliments:
        return None
    compliment = choice(compliments)
    compliment_index = int(compliment[0])
    database_update(compliment_index)
    compliment_text = compliment[1]
    return compliment_text


def get_all_compliments(count_of_page):
    all_compliments = []
    index = 0
    for page in range(1, count_of_page + 1):
        webpage = get(WEBSITE + '/page' + str(page)).text
        tags_of_compliments = BeautifulSoup(webpage, 'html.parser').find_all('div', {"class": "post-card__title"})
        for j in tags_of_compliments:
            all_compliments.append((index, j.text, 'No'))
            index += 1
    return all_compliments


def database_create():
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS compliments(
           compliment_id INT PRIMARY KEY,
           compliment TEXT,
           used TEXT);
        ''')
    CONNECT.commit()


def database_append(compliments_tuples):
    CURSOR.executemany('''INSERT INTO compliments VALUES(?, ?, ?);''', compliments_tuples)
    CONNECT.commit()


def database_update(compliment_id):
    sql = '''UPDATE compliments 
            SET used = 'Yes'
            WHERE compliment_id = (?)'''
    CURSOR.execute(sql, (compliment_id,))
    CONNECT.commit()


send_compliment()
