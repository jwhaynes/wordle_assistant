#wordle assistant in python

#import resources
import sqlite3
import re
import tkinter as tk

# create word database with sqlite3 python wrapper
db_connection = sqlite3.connect('wordle_list.db')

def regexp(pattern, searched_string):
    return re.fullmatch(pattern,searched_string) is not None

# make regexp function usable by the database connection and cursor
db_connection.create_function('regexp', 2, regexp)

# create database cursor to execute statements and fetch results
db_cursor = db_connection.cursor()

###################################################################
###### THE FOLLOWING CODE WAS USED TO INTIALIZE THE DATABASE ######
###################################################################

# make table in database with column for words
#db_cursor.execute('CREATE TABLE wordle_words(words)')

# check schema table to see that table exists
#res = db_cursor.execute('SELECT name FROM sqlite_master')
#print(res.fetchone())


### insert the words of the source text file into the sqlite3 database ###
#words_list = []
#with open('./python_wordle_assistant/wordle-nyt-words-14855.txt','r') as words_file:
#    file_lines = words_file.readlines()
#    for line in file_lines:
#        word = [line.strip()]
#        words_list.append(word)

#db_cursor.executemany('INSERT INTO wordle_words VALUES(?)', words_list)
#db_connection.commit()

#total_in_db = db_cursor.execute('SELECT * FROM wordle_words')
#print(len(total_in_db.fetchall()))

###################################################################
#################### END OF INITIALIZATION CODE ###################
###################################################################

letters = 'abcdefghijklmnopqrstuvwxyz'
letters_list = []
for letter in letters:
    letters_list.append(letter)


# letters in word
#good_letters = input('What letters are in the word?: ')

#bad_letters = input('What are the letters not in the word?: ')

good_letters = 'dodge'
bad_letters = 'z'


for letter in bad_letters:
    letters_list.remove(letter)
possible_letters = ''


for letter in letters_list:
    possible_letters = possible_letters + letter

pattern = 'aa(h|r|p)[a-z][a-z]'
#pattern = re.complie(r'(aa)|(ll)[a-z][a-z][a-z]')
#pattern = '[{good_letters}]|[{possible_letters}][{possible_letters}]|[{possible_letters}][{good_letters}]|[{possible_letters}][{good_letters}]|[{possible_letters}][{good_letters}]|[{possible_letters}]'.format(good_letters = good_letters, possible_letters=bad_letters)
matching_words = db_cursor.execute("SELECT * FROM wordle_words WHERE words REGEXP ?", [pattern] )


#matching_words = db_cursor.execute("SELECT * FROM wordle_words WHERE words REGEXP ?", [r'[dodge][dodge][dodge][dodge][dodge]'] )
print(matching_words.fetchall())

