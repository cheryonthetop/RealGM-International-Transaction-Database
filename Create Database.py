import sqlite3
from sqlite3 import Error
from urllib.request import urlopen
from bs4 import BeautifulSoup

file_path = "database.DB"


def create_tables(db_file):
    """
    establish a database connection to a SQLite database
    create the tables containing transactions for each season
    create the table containing every single transaction
    close the connection
    """
    conn = None
    cur = None
    url_template = "https://basketball.realgm.com/international/transactions/{year}"
    create_table_template = "CREATE TABLE IF NOT EXISTS transactions_{season} (" \
                            "month TEXT NOT NULL," \
                            "day TEXT NOT NULL," \
                            "transaction_num TEXT NOT NULL," \
                            "transaction_description TEXT NOT NULL);"
    insert_transaction_template = "INSERT INTO transactions_{season}(month, day, transaction_num, " \
                                  "transaction_description) VALUES (?, ?, ?, ?)"
    seasons = ["1213", "1314", "1415", "1516", "1617", "1718", "1819", "1920"]
    years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    try:
        # Get a connection and a cursor to execute sql commands
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # Create a table that contains all records of transactions (all season)
        create_table = "CREATE TABLE IF NOT EXISTS transactions (" \
                       "season TEXT NOT NULL," \
                       "month TEXT NOT NULL," \
                       "day TEXT NOT NULL," \
                       "transaction_num TEXT NOT NULL," \
                       "transaction_description TEXT NOT NULL);"

        cur.execute(create_table)

        for index in range(len(seasons)):
            # Create table for single-season transaction with the create_table query
            create_table = create_table_template.format(season=seasons[index])
            cur.execute(create_table)

            # Insert values into table

            # the url that contains the data we need
            url = url_template.format(year=years[index])

            # this is the html from the given url
            html = urlopen(url)

            # create a BeautifulSoup object by passing through html to the BeautifulSoup() constructor.
            # lxml is a html parser
            soup = BeautifulSoup(html, 'lxml')

            months = [m.getText() for m in soup.findAll("h2")]
            months = months[1:]

            days = [day.getText() for day in soup.findAll("h3")][:-8]

            daily_transactions = []
            # Get all the transactions from the given season
            for ul in soup.findAll("ul", style="padding-bottom: 15px; line-height: 1.5em;"):
                daily_transactions.append([li.getText() for li in ul.findAll("li")])

            day_index = 0
            month_index = 0
            mon = months[month_index][:-5]
            for transactions in daily_transactions:
                transaction_num = 1
                for transaction in transactions:
                    day = days[day_index]
                    day_no_comma = day.replace(",", "").replace(" ", "-")
                    transaction_no_stop = transaction.replace(".", "").replace(" ", "-")
                    if mon != day_no_comma.split("-")[0]:
                        month_index += 1
                        mon = months[month_index][:-5]
                    # Insert into the single-season table
                    params = (mon, day_no_comma, transaction_num, transaction_no_stop)
                    insert_transaction = insert_transaction_template.format(season=seasons[index])
                    cur.execute(insert_transaction, params)

                    # Insert into the all-in-one table
                    params = (seasons[index], mon, day_no_comma, transaction_num, transaction_no_stop)
                    insert_transaction = "INSERT INTO transactions(season, month, day, transaction_num, " \
                                         "transaction_description) VALUES (?, ?, ?, ?, ?)"
                    cur.execute(insert_transaction, params)
                    transaction_num += 1
                day_index += 1
    except Error as e:
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()
        print("connection closed")


if __name__ == '__main__':
    create_tables(db_file=file_path)