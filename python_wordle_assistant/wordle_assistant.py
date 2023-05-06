# import resources
import sqlite3
import re 
from tkinter import *
from tkinter import ttk

#create layout for app

class WordleAssistant:
    
    def __init__(self, parent):

        def make_entry_widgets(parent):
            entry_widgets = {}
            for num in range(1,6):
                entry_widgets[num] = ttk.Entry(parent,width=1,font=56)
                entry_widgets[num].grid(row=0,column=num, padx=10)

            return entry_widgets

        def make_check_boxes(parent):
            check_boxes = {}
            for entry in range(1,6):
                for row in range(1,6):
                    check_boxes[(entry, row)] = ttk.Checkbutton(parent,text="Not letter {}".format(row))
                    check_boxes[(entry, row)].grid(row=row,column=entry,padx=10)

            return check_boxes

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

        self.correct_letter_entry_widgets = make_entry_widgets(self.correct_letters_frame)

        s = ttk.Style()
        s.configure('My.TFrame', background='red')

        self.misplaced_letters_frame = ttk.LabelFrame(self.content_frame, text='Misplaced Letters', style='My.TFrame')
        self.misplaced_letters_frame.grid(row=1, column=0)

        self.misplaced_entry_widgets = make_entry_widgets(self.misplaced_letters_frame)
        
        self.misplaced_check_boxes = make_check_boxes(self.misplaced_letters_frame)

        self.incorrect_letters_frame = ttk.LabelFrame(self.content_frame, text='Incorrect Letters')
        self.incorrect_letters_frame.grid(row=2,column=0,sticky=(N))

        self.incorrect_letters_entry = ttk.Entry(self.incorrect_letters_frame, width=21)
        self.incorrect_letters_entry.grid(row=0,column=0)

        self.generate_guesses_button = ttk.Button(self.content_frame, text='Generate Guesses')
        self.generate_guesses_button.grid(row=3,column=0)

        self.guesses_label = ttk.Label(self.content_frame, text='Guesses', justify=['center'], font=50)
        self.guesses_label.grid(row=0, column=1, sticky=(S,))

        self.guesses_list = Listbox(self.content_frame, height=15)
        self.guesses_list.grid(row=1,column=1, rowspan=3)

        #self.content_frame.
    
    

        



def main():
    root = Tk()
    wordle_assistant = WordleAssistant(root)
    root.mainloop()

if __name__ == '__main__':
    main()



