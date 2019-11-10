import sqlite3
from sqlite3 import Error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import scrapy

# url that we are scraping
url = "https://basketball.realgm.com/international/transactions/2018"

# this is the html from the given url
html = urlopen(url)

# create a BeautifulSoup object by passing through html to the BeautifulSoup() constructor.
# lxml is a html parser
soup = BeautifulSoup(html, 'lxml')

months = [month.getText() for month in soup.findAll("h2")]
season = months[0][:10]
print(months)
print(season)

days = [day.getText() for day in soup.findAll("h3")][:-8]
print(days)
print(len(days))

daily_transactions = []
for ul in soup.findAll("ul", style="padding-bottom: 15px; line-height: 1.5em;"):
    daily_transactions.append([li.getText for li in ul.findAll("li")])

print(len(daily_transactions))


'''
file_path = "database.DB"



def create_database(db_file):
    """
    create a database connection to a SQLite database
    generate the database
    close the connection
    """
    conn = None
    cur = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cur = conn.cursor()
        create_table = "CREATE TABLE IF NOT EXISTS transactions (" \
                       "year INTEGER NOT NULL," \
                       "month TEXT NOT NULL," \
                       "day INTEGER NOT NULL," \
                       "transaction_num INTEGER NOT NULL," \
                       "transaction_description TEXT NOT NULL)"
        cur.execute(create_table)
        
    except Error as e:
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_database(db_file=file_path)
'''
