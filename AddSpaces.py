import re

quran = open("Docs/Quran.txt", "r")
quranWithSpaces = open("Docs/quranWithSpaces.txt", "w")
quranWithLines = open("Docs/quranWithLines.txt", "w")
# read data and split into words
quranText = quran.read()
quranText = quranText.splitlines(True)

#quranWithLines.writelines(quranText)

for line in quranText:
        line = line.replace('\n', ' ') # replace new line with spaces
        index = line.rfind('|')
        quranWithSpaces.write(line[:index+1])
        quranWithSpaces.write(" ")
        quranWithSpaces.write(line[index+1:])
        quranWithSpaces.write("_")
        quranWithSpaces.write(" ")
        