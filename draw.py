# !/usr/bin/python3

import tkinter
from tkinter import scrolledtext, ttk
import random
import math

DEBUG = False
INF = 10e9

window = tkinter.Tk()
window.geometry("1280x800")
version = "3.1"
window.title("Memo version:" + version)


# w, h = window.winfo_screenwidth(), window.winfo_screenheight()
# window.geometry("%dx%d+0+0" % (w, h))
# print(w, h)


class Word:
    def __init__(self):
        self.weight = 0
        self.translates = set()

    def __init__(self, translate: list):
        self.weight = 0
        self.translates = set(translate)

    def up(self):
        self.weight += 1

    def down(self):
        self.weight -= 1


def word_and_translate(word):
    all_translates = word + " " + "-" + " "
    for _translate in dictionary[word].translates:
        all_translates += _translate
        all_translates += " "
    return all_translates


def read_dictionary():
    global dictionary
    dictionary = dict()
    vocabluary.seek(0)
    for line in vocabluary.read().split("\n"):
        if len(line) > 1:
            _line = line.split()
            word = _line[0]
            translates = _line[2:]
            dictionary[word] = Word(translates)


def clear() -> None:
    objects = set(window.place_slaves())
    for obj in objects:
        obj.place_forget()

    emblem = tkinter.Label(window, text="Memo", font=("Helvetica Neue", 64), foreground="blue")
    info = tkinter.Label(window, text="Бурмистров Влад, 2021", font=("Helvetica", 20))

    info.place(x=900, y=650)
    emblem.place(x=50, y=50)


def display_button_back():
    button_back = tkinter.Button(window, text="Назад", width=20, height=5, command=display_introduction)
    button_back.place(x=85, y=550)


def display_static():
    clear()
    display_button_back()

    all_text = ""
    for word in dictionary:
        all_text += word
        all_text += "\t \t"
        for translate in dictionary[word].translates:
            all_text += translate
            all_text += "\t \t \t"
        all_text += str(dictionary[word].weight)
        all_text += "\t \t"
        if dictionary[word].weight >= 10:
            all_text += "Усвоено"
        else:
            all_text += "Не усвоено"
        all_text += "\n"

    text = tkinter.Label(window, text="Слово \t \t Перевод \t \t Уровень \t Статус", font=("Helvetica Bold", 20))
    static = scrolledtext.ScrolledText(window, width=70, height=23, font=("Helvetica", 20))
    static.insert(2.0, all_text)
    static.configure(state='disabled')

    static.place(x=350, y=100)
    text.place(x=350, y=50)


def display_select_module():
    global all_vocabluaries, vocabluary, combo

    clear()
    display_button_back()

    text_change = tkinter.Label(window, text="Выберите модуль:", font=("Helvetica", 20))

    def update():
        global all_vocabluaries
        all_vocabluaries.seek(0)
        combo["values"] = all_vocabluaries.read()

    combo = ttk.Combobox(window, postcommand=update)
    combo.config(state="readonly")

    text_new_module = tkinter.Label(window, text="Или создайте новый:", font=("Helvetica", 20))
    text_new_name = tkinter.Label(window, text="Введите название:", font=("Helvetica", 20))
    new_module = tkinter.Entry(window)

    def add_vocabluary():
        global all_vocabluaries, vocabluary
        vocabluary_name = new_module.get()
        all_vocabluaries.write(vocabluary_name + '\n')
        all_vocabluaries.flush()
        vocabluary.close()
        vocabluary = open(vocabluary_name + ".txt", "w+")
        read_dictionary()


    def safe_choice():
        global vocabluary
        vocabluary.flush()
        vocabluary.close()
        vocabluary = open(combo.get() + ".txt", "r+")
        vocabluary.seek(0)
        read_dictionary()


    button_safe = tkinter.Button(window, text="Сохранить", command=add_vocabluary)
    button_safe_choice = tkinter.Button(window, text="Сохранить", command=safe_choice)

    text_change.place(x=300, y=200)
    combo.place(x=500, y=200)
    text_new_module.place(x=300, y=350)
    text_new_name.place(x=300, y=400)
    new_module.place(x=500, y=400)
    button_safe.place(x=700, y=400)
    button_safe_choice.place(x=725, y=200)


def display_change_module():
    global text, vocabluary
    clear()
    display_button_back()

    def safe_changes_text():
        vocabluary.seek(0)
        vocabluary.truncate()
        for line in text.get("1.0", tkinter.END).split("\n"):
            vocabluary.write(line + "\n")
            vocabluary.flush()
        read_dictionary()

    text_head = tkinter.Label(window, text="Слово \t \t Перевод", font=("Helvetica Bold", 20))
    button_safe = tkinter.Button(window, width=25, height=7, text="Сохранить", command=safe_changes_text)
    text = scrolledtext.ScrolledText(window, width=50, height=23, font=("Helvetica", 20))
    vocabluary.seek(0)
    text.insert(2.0, vocabluary.read())

    button_safe.place(x=1000, y=100)
    text.place(x=350, y=100)
    text_head.place(x=350, y=50)


def learning():
    global translate, word, button_unknow, label_word, word, progress

    clear()

    word = ""
    weight = INF
    print(list(dictionary.keys()))
    _list = list(dictionary.keys())
    random.shuffle(_list)
    for _word in _list:
        if dictionary[_word].weight < weight:
            weight = dictionary[_word].weight
            word = _word

    def unknow():
        clear()

        all_translates = word_and_translate(word)
        dictionary[word].down()
        lable_word_translate = tkinter.Label(window, text=all_translates, font=("Helvetica Neue", 64))
        button_next = tkinter.Button(window, text="Продолжить", command=learning, width=20, height=5)

        lable_word_translate.place(x=400, y=125)
        button_next.place(x=500, y=300)

        display_button_back()

    def check_ans():
        global learned, all_words_cnt, progress
        button_unknow.place_forget()

        all_translates = word_and_translate(word)
        label_word.config(text=all_translates)

        translate.config(state="readonly")

        if translate.get() in dictionary[word].translates:
            status = tkinter.Label(window, font=("Helvetica Neue", 60), foreground="green", text="ok")
            status.place(x=525, y=350)
            dictionary[word].up()
            learned = min(all_words_cnt, learned + 1)
            # progress.step(0.1)
        else:
            status = tkinter.Label(window, font=("Helvetica Neue", 60), foreground="red", text="Неправильно")
            status.place(x=400, y=350)
            dictionary[word].down()
            learned = max(0, learned - 1)

        print(round(learned / all_words_cnt) * 100)
        progress.config(value=round(learned / all_words_cnt) * 100)
        next = tkinter.Button(window, text="Далее", command=learning, width=17, height=5)
        next.place(x=500, y=500)

    label_word = tkinter.Label(window, text=word, font=("Helvetica Neue", 60))
    translate = tkinter.Entry(window)
    button_check = tkinter.Button(window, text="Проверить", command=check_ans)
    button_unknow = tkinter.Button(window, text="Не знаю", command=unknow, width=17, height=5)

    translate.focus()

    button_unknow.place(x=500, y=400)
    translate.place(x=450, y=300)
    button_check.place(x=650, y=300)
    label_word.place(x=500, y=150)
    display_button_back()


def cards():
    global button_word, word

    clear()

    def reverse2():
        button_word.config(text=word, command=reverse)

    def reverse():
        all_translate = ""
        for _translate in dictionary[word].translates:
            all_translate += _translate
            all_translate += " "

        button_word.config(text=all_translate, command=reverse2)

    word = random.choice(list(dictionary.keys()))
    button_next = tkinter.Button(window, text="Далее", width=25, height=6, command=cards)
    # button_back = tkinter.Button(window, text="Назад", width=25, height=6)
    button_word = tkinter.Button(window, text=word, width=55, height=20, command=reverse)

    # button_back.place(x=400, y=450)
    button_next.place(x=525, y=450)
    button_word.place(x=400, y=100)

    display_button_back()


def display_introduction():
    global progress
    clear()

    button_card = tkinter.Button(window, width=50, height=10, text="Карточки.", command=cards)
    button_learning = tkinter.Button(window, width=50, height=10, text="Продолжить заучивание.", command=learning)
    button_learning.focus()

    button_change_module = tkinter.Button(window, width=30, height=5, text="Изменить модуль.",
                                          command=display_change_module)
    button_statics = tkinter.Button(window, width=30, height=5, text="Просмотр статистики.", command=display_static)
    button_select_module = tkinter.Button(window, width=30, height=5, text="Выбрать другой модуль.",
                                          command=display_select_module)


    progress = ttk.Progressbar(window, orient="horizontal", length=450, value=0)


    emblem = tkinter.Label(window, text="Memo", font=("Helvetica Neue", 64), foreground="blue")
    info = tkinter.Label(window, text="Бурмистров Влад, 2021", font=("Helvetica", 20))

    info.place(x=900, y=650)
    emblem.place(x=50, y=50)

    if DEBUG:
        button_card.place(x=300, y=285)
        button_change_module.place(x=800, y=100)
        button_learning.place(x=300, y=100)
        button_statics.place(x=800, y=200)
        button_select_module.place(x=800, y=300)
        progress.place(x=300, y=500)
    else:
        button_card.place(x=300, y=285)
        button_change_module.place(x=800, y=100)
        button_learning.place(x=300, y=100)
        button_statics.place(x=800, y=200)
        button_select_module.place(x=800, y=300)


# files
all_vocabluaries = open("all_vocabluaries.txt", "r+")
vocabluary = open("vocabluary.txt", "r+")

dictionary = dict()
read_dictionary()

learned = 0
all_words_cnt = len(dictionary) * 10


# necessary for strart programm
display_introduction()

tkinter.mainloop()
