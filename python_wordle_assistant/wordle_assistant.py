# import resources
import sqlite3
import re 
from tkinter import *
from tkinter import ttk
from wordle_assistant_db_setup import search_wordle_list_db

#create layout for app

class WordleAssistant:
    
    def __init__(self, parent):

        def make_entry_widgets(parent):
            parent.entry_widgets = {}
            parent.entry_widgets_values = {}
            for num in range(1,6):
                parent.entry_widgets_values[num] = StringVar('')
                parent.entry_widgets[num] = ttk.Entry(parent,width=2,font=56, textvariable=parent.entry_widgets_values[num])
                parent.entry_widgets[num].grid(row=0,column=num, padx=10)

        def make_check_boxes(parent):
            parent.check_boxes = {}
            parent.check_boxes_values = {}
            for entry in range(1,6):
                for row in range(1,6):
                    parent.check_boxes_values[(entry, row)] = BooleanVar(False)
                    parent.check_boxes[(entry, row)] = ttk.Checkbutton(parent,text="Not letter {}".format(row),variable=parent.check_boxes_values[(entry,row)],onvalue=True,offvalue=False)
                    parent.check_boxes[(entry, row)].grid(row=row,column=entry,padx=10)
        
        def generate_guesses(self):
            letters = 'abcdefghijklmnopqrstuvwxyz'
            letters_list = []
            for letter in letters:
                letters_list.append(letter)

            positions = {
                1: '',
                2: '',
                3: '',
                4: '',
                5: ''
            }

            for (key, value) in self.correct_letters_frame.entry_widgets_values.items():
                if value.get() != '':
                    positions[key] = value.get()
            
            for letter in self.incorrect_letters_entry_value.get():
                if letter in letters_list:
                    letters_list.remove(letter)
            
            possible_letters = ''
            for letter in letters_list:
                possible_letters = possible_letters + letter

            possible_letters = '[' + possible_letters + ']'
            
            for (key, value) in positions.items():
                if value == '':
                    positions[key] = possible_letters
            
            pattern = positions[1] + positions[2] + positions[3] + positions[4] + positions[5]
            print(pattern)
            word_list_tuples = search_wordle_list_db(pattern)

            word_guesses_list = []
            for word in word_list_tuples:
                word_guesses_list.append(word[0])
            
            self.word_list = word_guesses_list
            self.listbox_words.set(self.word_list)

        self.parent = parent
        self.parent.title('Wordle Assistant by Jay Haynes')
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=20)

        self.title = ttk.Label(self.parent, text='Wordle Assistant', justify=['center'], font=200)
        self.title.grid(row=0, column=0, pady=10)

        self.content_frame = ttk.Frame(self.parent, padding=10)
        self.content_frame.grid(row=1, column=0)

        self.content_frame.columnconfigure(0, weight=3)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        self.content_frame.rowconfigure(3, weight=1)

        self.correct_letters_frame = ttk.LabelFrame(self.content_frame, text='Correct Letters')
        self.correct_letters_frame.grid(row=0,column=0,sticky=(N,S))

        make_entry_widgets(self.correct_letters_frame)

        self.misplaced_letters_frame = ttk.LabelFrame(self.content_frame, text='Misplaced Letters')
        self.misplaced_letters_frame.grid(row=1, column=0)

        make_entry_widgets(self.misplaced_letters_frame)
        
        make_check_boxes(self.misplaced_letters_frame)

        self.incorrect_letters_frame = ttk.LabelFrame(self.content_frame, text='Incorrect Letters')
        self.incorrect_letters_frame.grid(row=2,column=0,sticky=(N))

        self.incorrect_letters_entry_value = StringVar('')
        self.incorrect_letters_entry = ttk.Entry(self.incorrect_letters_frame, width=21, textvariable=self.incorrect_letters_entry_value)
        self.incorrect_letters_entry.grid(row=0,column=0)

        self.generate_guesses_button = ttk.Button(self.content_frame, text='Generate Guesses', command= lambda: generate_guesses(self))
        self.generate_guesses_button.grid(row=3,column=0)

        
        self.guesses_label = ttk.Label(self.content_frame, text='Guesses', justify=['center'], font=50)
        self.guesses_label.grid(row=0, column=1, sticky=(S,))

        self.word_list = ['Welcome', 'to', 'Wordle', 'Assistant']
        self.listbox_words = StringVar(value=self.word_list)
        self.guesses_list = Listbox(self.content_frame, height=15, listvariable=self.listbox_words)
        self.guesses_list.grid(row=1,column=1, rowspan=3)
    
    

        



def main():
    root = Tk()
    wordle_assistant = WordleAssistant(root)
    root.mainloop()

if __name__ == '__main__':
    main()



