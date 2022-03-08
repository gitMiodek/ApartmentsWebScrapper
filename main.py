from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv
import pandas as pd

db = sqlite3.connect('data.db')
cursor = db.cursor()
query = 'DELETE FROM apartaments'
cursor.execute(query)
if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute(''' CREATE TABLE aparatments (title TEXT, price REAL, location TEXT, area TEXT)''')

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/'
page = get(URL)
bs = BeautifulSoup(page.content)


def price_format(price):
    return float(price.replace(' ', '').replace('zł', ''))


for offer in bs.find_all('div', class_='offer-wrapper'):
    bot_cel = offer.find('td', class_="bottom-cell")  #
    location = bot_cel.find('small', class_='breadcrumb').get_text().strip().split(',')[1]
    title = offer.find('strong').get_text().strip()
    price = price_format(offer.find('p', class_='price').get_text().strip())
    link = offer.find('a')['href']
    link_page = get(link)
    ls = BeautifulSoup(link_page.content)
    try:
        area = ls.find('ul', class_='css-sfcl1s').get_text().split()[5]
        print(area)
    except:
        area = None
        print(area)

    cursor.execute('INSERT INTO apartaments VALUES(?,?,?,?)', (title, price, location, area))
    db.commit()
db.close()
path = '/home/jakub/PycharmProjects/WebScrapping/data.db'

con = sqlite3.Connection(path)

query = """
SELECT *
FROM apartaments;
"""
observations = pd.read_sql(query, con)

print(observations)
