# import resources
import sqlite3
import re 
from tkinter import *
from tkinter import ttk
from wordle_assistant_db_setup import search_wordle_list_db

#create layout for app within wordle assistant class
class WordleAssistant:
    ## init with tk root as parent
    def __init__(self, parent):
        
        # validation function for use with entrybox widgets (limits input to 1 lower case letter character)
        def check_entry(newval):
            return re.match(r'^[a-z]|\s*$', newval) is not None and len(newval) <= 1
        
        # create wrapper for validation function and register with root
        check_entry_wrapper = (parent.register(check_entry), '%P')

        # method to create entry widgets
        def make_entry_widgets(parent):
            # create dictionary to hold entry widgets as a property of a parent (a label frame)
            parent.entry_widgets = {}
            # create dictionary to hold values associated with entry widgets (also a property of label frame parent)
            parent.entry_widgets_values = {}
            # loop to create five widgets (one for each wordle letter) and associated string variable values
            for num in range(1,6):
                parent.entry_widgets_values[num] = StringVar('')
                parent.entry_widgets[num] = ttk.Entry(parent,width=2,font=56, textvariable=parent.entry_widgets_values[num], validate='key', validatecommand=check_entry_wrapper)
                parent.entry_widgets[num].grid(row=0,column=num, padx=10)

        # method to create check boxes
        def make_check_boxes(parent):
            # create dictionary to hold check box widgets as a property of label frame parent
            parent.check_boxes = {}
            # create dictionary to hold check box widget values (boolean) as a property of a label frame parent
            parent.check_boxes_values = {}
            # loop with nested loop to create five check boxes for each entry box and an associated boolean variable
            for entry in range(1,6):
                for row in range(1,6):
                    parent.check_boxes_values[(entry, row)] = BooleanVar(False)
                    parent.check_boxes[(entry, row)] = ttk.Checkbutton(parent,text="Not letter {}".format(row),variable=parent.check_boxes_values[(entry,row)],onvalue=True,offvalue=False)
                    parent.check_boxes[(entry, row)].grid(row=row,column=entry,padx=10)
        
        # method called whenever "generate guesses" button is pushed
        def generate_guesses(self):
            letters = 'abcdefghijklmnopqrstuvwxyz' # all possible lowercase letters
            letters_list = [] # list to hold all possible lowercase letters
            for letter in letters:
                letters_list.append(letter)

            # strings that will represent the regex patterns for each letter position
            positions = {
                1: '',
                2: '',
                3: '',
                4: '',
                5: ''
            }

            # look at correct letter entries; if a letter is placed that letter becomes the position specific regex pattern
            for (key, value) in self.correct_letters_frame.entry_widgets_values.items():
                if value.get() != '':
                    positions[key] = value.get()
            
            # look at letters in incorrect letter entries; remove these letters from letter_list
            for letter in self.incorrect_letters_entry_value.get():
                if letter in letters_list:
                    letters_list.remove(letter)
            
            # create a dictionary to hold position specific list of possible letters 
            # (like positions but a dictionary of lists instead of a dictionary of strings)
            position_letters_list = {num:[] for num in positions.keys()}
            for position in position_letters_list.keys():
                for letter in letters_list:
                    position_letters_list[position].append(letter)

            # create a list to hold postive look-ahead assertion (make sure misplaced letters are in word)
            positive_look_ahead_assertions = []

            # loop through misplaced letter entry values (goal is to remove misplaced letters from position lists they don't belong in)
            for (key,value) in self.misplaced_letters_frame.entry_widgets_values.items():
                if value.get() != '': # determine if a specific entry is empty or not
                    entry_value_letter = value.get() # extract misplaced letter value
                    positive_look_ahead_assertions.append('(?=.*{letter}.*)'.format(letter=entry_value_letter)) # create a positive look ahead assertion for misplaced letter
                    # loop through checkboxes to determine in which position lists to eliminate the letter
                    for (checkbutton,value) in self.misplaced_letters_frame.check_boxes_values.items():
                        if (checkbutton[0] == key) and (value.get() == True): # make sure checkbox is in the correct column
                            if entry_value_letter in position_letters_list[checkbutton[1]]: # determine if letter is in position associated list
                                position_letters_list[checkbutton[1]].remove(entry_value_letter) # remove letter as a possibility at this position
                                

            # define dictionary to hold regex string for each letter position
            possible_letters_strings = {}
            # loop through each list in position_letters_list dictionary
            for (num,letter_list) in position_letters_list.items():
                # following code puts all possible letters for a position in a character class
                possible_letters_strings[num] = '['
                for letter in letter_list:
                    possible_letters_strings[num] = possible_letters_strings[num] + letter
                possible_letters_strings[num] = possible_letters_strings[num] + ']'
            
            # if correct letter isn't known for a position -> place appropriate regex expression as value
            for (key, value) in positions.items():
                if value == '':
                    positions[key] = possible_letters_strings[key]
            
            #sum up regex expressions (as assigned in positions dictionary) into a single string
            pattern = positions[1] + positions[2] + positions[3] + positions[4] + positions[5]

            # put positive look ahead assertions at beggining of regex pattern
            for assertion in positive_look_ahead_assertions:
                pattern = assertion + pattern

            # call imported function to query sqlite database for word matches
            word_list_tuples = search_wordle_list_db(pattern)

            # convert list of tuples into a list of strings
            word_guesses_list = []
            for word in word_list_tuples:
                word_guesses_list.append(word[0])
            
            # set the list of word guesses as a property
            self.word_list = word_guesses_list
            # link the list of word guesses to listbox for display
            self.listbox_words.set(self.word_list)

        # set some properties for root (weight properties for resizing)
        self.parent = parent
        self.parent.title('Wordle Assistant by Jay Haynes')
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=20)

        # create app title and grid
        self.title = ttk.Label(self.parent, text='Wordle Assistant', justify=['center'], font=200)
        self.title.grid(row=0, column=0, pady=10)

        # create content frame for gridding
        self.content_frame = ttk.Frame(self.parent, padding=10)
        self.content_frame.grid(row=1, column=0)

        # set some content frame properties (weight properties for resizing)
        self.content_frame.columnconfigure(0, weight=3)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        self.content_frame.rowconfigure(3, weight=1)

        # create a "correct letters" label frame to hold correct letter entry widgets
        self.correct_letters_frame = ttk.LabelFrame(self.content_frame, text='Correct Letters')
        self.correct_letters_frame.grid(row=0,column=0,sticky=(N,S))

        # call method to make entry widgets in label frame
        make_entry_widgets(self.correct_letters_frame)

        # create a "misplaced letters" label frame to hold misplaced letter entry widgets
        self.misplaced_letters_frame = ttk.LabelFrame(self.content_frame, text='Misplaced Letters')
        self.misplaced_letters_frame.grid(row=1, column=0)

        # call method to make entry widgets in label frame
        make_entry_widgets(self.misplaced_letters_frame)
        
        # call method to make check boxes in label frame
        make_check_boxes(self.misplaced_letters_frame)

        # create an "incorrect letters" label frame to hold an incorrect letters entry widget
        self.incorrect_letters_frame = ttk.LabelFrame(self.content_frame, text='Incorrect Letters')
        self.incorrect_letters_frame.grid(row=2,column=0,sticky=(N))

        # create an incorrect letters entry widget and associated variable
        self.incorrect_letters_entry_value = StringVar('')
        self.incorrect_letters_entry = ttk.Entry(self.incorrect_letters_frame, width=21, textvariable=self.incorrect_letters_entry_value)
        self.incorrect_letters_entry.grid(row=0,column=0)

        # create a button for generating guesses (generate guesses function is command)
        self.generate_guesses_button = ttk.Button(self.content_frame, text='Generate Guesses', command= lambda: generate_guesses(self))
        self.generate_guesses_button.grid(row=3,column=0)

        # create a label for "guesses" listbox
        self.guesses_label = ttk.Label(self.content_frame, text='Guesses', justify=['center'], font=50)
        self.guesses_label.grid(row=0, column=1, sticky=(S,))

        # create a listbox and scroll bar and associated variables to hold word guesses
        self.word_list = ['Welcome', 'to', 'Wordle', 'Assistant']
        self.listbox_words = StringVar(value=self.word_list)
        self.guesses_list = Listbox(self.content_frame, height=15, listvariable=self.listbox_words)
        self.guesses_list.grid(row=1,column=1, rowspan=3)
        self.listbox_scroll = ttk.Scrollbar(self.content_frame, orient=VERTICAL, command=self.guesses_list.yview)
        self.listbox_scroll.grid(row=1,column=2, rowspan=3, sticky=(N,S))
        self.guesses_list.configure(yscrollcommand=self.listbox_scroll.set)
    
    

        



# instantiate root and world_assistant class and event loop
def main():
    root = Tk()
    wordle_assistant = WordleAssistant(root)
    root.mainloop()

# call main if this script is being run
if __name__ == '__main__':
    main()



