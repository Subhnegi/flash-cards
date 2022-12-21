from random import choice
from tkinter import messagebox
from numpy import tile
import pandas
from tkinter import *
import os
BACKGROUND_COLOR = "#B1DDC6"

try:
    french_data = pandas.read_csv("./data/wordstolearn.csv")
except FileNotFoundError:
    french_data = pandas.read_csv("./data/french_words.csv")
french_dict = french_data.to_dict(orient="records")
current_card={}

#============================ flip card===============================#


def flip_card():
    canvas.itemconfigure(img,image=card_back_img)
    canvas.itemconfigure(card_word, text=current_card["English"],fill="White")
    canvas.itemconfigure(language, text="English",fill="White")

    #============================ next card===============================#


def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = choice(french_dict)
    except IndexError:
        messagebox.showinfo(title="WOHOOOO!!!",message="There are no more words left")
    else:
        french_word = current_card["French"]
        canvas.itemconfigure(card_word, text=french_word,fill="Black")
        canvas.itemconfigure(language, text="French",fill="Black")
        canvas.itemconfigure(img,image=card_front_img)
        flip_timer=window.after(3000, flip_card)

def learned():
    try:
        french_dict.remove(current_card)
    except ValueError:
        messagebox.showinfo(title="WOHOOOO!!!",message="You have sucessfully learned every word")
        os.remove("./data/wordstolearn.csv")
    try:
        next_card()
        new_dict=pandas.DataFrame.from_dict(french_dict)
        new_dict.to_csv("./data/wordstolearn.csv")
    except IndexError:
        messagebox.showinfo(title="WOHOOOO!!!",message="You have sucessfully learned every word")
    



#============================ UI setup===============================#
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer=window.after(3000, flip_card)

canvas = Canvas(width=800, height=526,
                highlightthickness=0, bg=BACKGROUND_COLOR)
card_back_img = PhotoImage(file=".\images\card_back.png")
card_front_img = PhotoImage(file=".\images\card_front.png")
img = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=learned)
right_button.grid(row=1, column=0)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=1)

next_card()


window.mainloop()
