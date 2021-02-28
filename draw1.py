import tkinter
import classes
from tkinter import scrolledtext, ttk

try:
    import main
except:
    pass

window = tkinter.Tk()
window.geometry("1280x800")
version = "2.1"
window.title("Memo version:" + version)


# w, h = window.winfo_screenwidth(), window.winfo_screenheight()
# window.geometry("%dx%d+0+0" % (w, h))
# print(w, h)


def clear() -> None:
    global objects
    for obj in objects:
        obj.place_forget()
    objects = set()


def display_button_back():
    button_back = tkinter.Button(window, text="Назад", width=20, height=5, command=display_introduction)
    objects.add(button_back)
    button_back.place(x=85, y=550)


def display_static():
    clear()
    display_button_back()

    text = tkinter.Label(window, text="Слово \t \t Перевод \t \t \t Уровень \t Статус", font=("Helvetica Bold", 20))
    static = scrolledtext.ScrolledText(window, width=70, height=23, font=("Helvetica", 20))
    static.insert(2.0, vocabluary.read())
    static.configure(state='disabled')

    static.place(x=350, y=100)
    text.place(x=350, y=50)

    objects.add(static)
    objects.add(text)


def display_select_module():
    global all_vocabluaries
    clear()
    display_button_back()

    text_change = tkinter.Label(window, text="Выберите модуль:", font=("Helvetica", 20))

    combo = ttk.Combobox(window)
    combo['values'] = all_vocabluaries.read()
    combo.config(state="readonly")

    text_new_module = tkinter.Label(window, text="Или создайте новый:", font=("Helvetica", 20))
    text_new_name = tkinter.Label(window, text="Введите название:", font=("Helvetica", 20))
    new_module = tkinter.Entry(window)

    def add_vocabluary():
        global all_vocabluaries, vocabluary
        vocabluary_name = new_module.get()
        all_vocabluaries.write(vocabluary_name + '\n')
        all_vocabluaries.close()
        all_vocabluaries = open("all_vocabluaries.txt", "r+")
        vocabluary.close()
        vocabluary = open(vocabluary_name + ".txt", "tw+")
    button_safe = tkinter.Button(window, text="Сохранить", command=add_vocabluary)

    text_change.place(x=300, y=200)
    combo.place(x=500, y=200)
    text_new_module.place(x=300, y=350)
    text_new_name.place(x=300, y=400)
    new_module.place(x=500, y=400)
    button_safe.place(x=700, y=400)

    objects.add(combo)
    objects.add(text_change)
    objects.add(text_new_module)
    objects.add(text_new_name)
    objects.add(new_module)
    objects.add(button_safe)


def display_change_module():
    clear()
    display_button_back()

    text = scrolledtext.ScrolledText(window, width=50, height=23, font=("Helvetica", 20))
    text.insert(2.0, vocabluary.read())

    text.place(x=350, y=100)

    objects.add(text)


def display_introduction():
    clear()

    button_learning = tkinter.Button(window, width=50, height=20, text="Продолжить заучивание.")

    button_learning.focus()

    button_change_module = tkinter.Button(window, width=30, height=5, text="Изменить модуль.",
                                          command=display_change_module)
    button_statics = tkinter.Button(window, width=30, height=5, text="Просмотр статистики.", command=display_static)
    button_select_module = tkinter.Button(window, width=30, height=5, text="Выбрать другой модуль.",
                                          command=display_select_module)
    progress = ttk.Progressbar(window, orient="horizontal", length=450)
    emblem = tkinter.Label(window, text="Memo", font=("Helvetica Neue", 64), foreground="blue")
    info = tkinter.Label(window, text="Бурмистров Влад, 2021", font=("Helvetica", 20))

    info.place(x=900, y=650)
    emblem.place(x=50, y=50)

    button_change_module.place(x=800, y=100)
    button_learning.place(x=300, y=100)
    button_statics.place(x=800, y=200)
    button_select_module.place(x=800, y=300)
    progress.place(x=300, y=500)

    objects.add(button_learning)
    objects.add(button_select_module)
    objects.add(button_statics)
    objects.add(button_change_module)
    objects.add(progress)


# files
vocabluary = open("vocabluary.txt", "r+")
all_vocabluaries = open("all_vocabluaries.txt", "r+")

# necessary for strart programm
objects = set()
display_introduction()

tkinter.mainloop()
