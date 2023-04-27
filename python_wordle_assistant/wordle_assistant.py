#wordle assistant in python

#import resources
import sqlite3

# create word database with sqlite3 python wrapper
db_connection = sqlite3.connect('wordle_list.db')

# create database cursor to execute statements and fetch results
db_cursor = db_connection.cursor()

# make table in database with column for words
#db_cursor.execute('CREATE TABLE wordle_words(words)') ### commented out because table only needs to be created once ###

# check schema table to see that table exists
res = db_cursor.execute('SELECT name FROM sqlite_master')
print(res.fetchone())