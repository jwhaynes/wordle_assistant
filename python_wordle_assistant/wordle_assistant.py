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
#res = db_cursor.execute('SELECT name FROM sqlite_master')
#print(res.fetchone())


### insert the words of the source text file into the sqlite3 database ###
words_list = []
with open('./python_wordle_assistant/wordle-nyt-words-14855.txt','r') as words_file:
    file_lines = words_file.readlines()
    for line in file_lines:
        word = [line.strip()]
        words_list.append(word)

#db_cursor.executemany('INSERT INTO wordle_words VALUES(?)', words_list)
#db_connection.commit()

total_in_db = db_cursor.execute('SELECT * FROM wordle_words')
print(len(total_in_db.fetchall()))