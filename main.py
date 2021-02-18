def new_word(word: str, translate: str) -> None:
    if word in words:
        translates[word].add(translate)
    else:
        words.add(word)
        translates[word] = set()
        translates[word].add(translate)
        

translates = dict()
words = set()
file = open("vocabluary.txt", mode="r+", encoding="UTF-8")
text_of_file = file.read()

for line in file:
    _word, _translate = line.split()
    words.add(_word)
    new_word(_word, _translate)

file.seek(0)
file.truncate()
new_word("hello", "bye")

for word in translates:
    file.write(word + " ")
    for w in translates[word]:
        file.write(w + " ")
    file.write("\n")
