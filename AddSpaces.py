import re

quran = open("Docs/Quran.txt", "r")
quranWithSpaces = open("Docs/quranWithSpaces.txt", "w")
# read data and split into words
quranText = quran.read()
quranText = quranText.split()

index = 0
first = False
for word in quranText: 
    if (index != len(quranText)-1):
        if (re.match(r"[0-9]+\|[0-9]+\|", word)):
            if (first):
                quranWithSpaces.write("_ ")
            pipe_index = word.rfind('|')
            quranWithSpaces.write(word[:pipe_index+1])
            quranWithSpaces.write(" ")
            quranWithSpaces.write(word[pipe_index+1:])
            quranWithSpaces.write(" ")
            first = True
        else:
            quranWithSpaces.write(word)
            quranWithSpaces.write(" ")
    else:
        quranWithSpaces.write(word)
    index += 1