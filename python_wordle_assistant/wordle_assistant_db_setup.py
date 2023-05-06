#wordle assistant in python

#import resources
import sqlite3
import re

# create word database with sqlite3 python wrapper
#db_connection = sqlite3.connect('wordle_list.db')

# make regexp function usable by the database connection and cursor
#db_connection.create_function('regexp', 2, regexp)

# create database cursor to execute statements and fetch results
#db_cursor = db_connection.cursor()

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


def search_wordle_list_db(pattern):
    # create word database with sqlite3 python wrapper
    db_connection = sqlite3.connect('wordle_list.db')

    #regexp function used in db query
    def regexp(pattern, searched_string):
        return re.fullmatch(pattern,searched_string) is not None
    
    # make regexp function usable by the database connection and cursor
    db_connection.create_function('regexp', 2, regexp)

    # create database cursor to execute statements and fetch results
    db_cursor = db_connection.cursor()

    # query for words that match pattern
    matching_words = db_cursor.execute("SELECT * FROM wordle_words WHERE words REGEXP ?", [pattern] )

    # turn query into a list
    matching_words_list = matching_words.fetchall()

    #close connection to database
    db_connection.close()

    return matching_words_list


letters = 'abcdefghijklmnopqrstuvwxyz'
letters_list = []
for letter in letters:
    letters_list.append(letter)

bad_letters = 'aieuthrnmb'


for letter in bad_letters:
    letters_list.remove(letter)

possible_letters = ''
for letter in letters_list:
    possible_letters = possible_letters + letter


pos1 = 'd'
pos2 = '[' + possible_letters + ']'
pos3 = '[' + possible_letters + ']'
pos4 = '[' + possible_letters + ']'
pos5 = '[' + possible_letters + ']'

pattern = pos1 + pos2 + pos3 + pos4 + pos5

matches = search_wordle_list_db(pattern)
print(matches)
for match in matches:
    if 'o' in match:
        print(match)