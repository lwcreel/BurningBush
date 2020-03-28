import re

quran = open("Docs/Quran.txt", "r")
quranWithSpaces = open("Docs/quranWithSpaces.txt", "w")
quranWithLines = open("Docs/quranWithLines.txt", "w")
# read data and split into words
quranText = quran.read()
quranText = quranText.splitlines(True)

#quranWithLines.writelines(quranText)

for line in quranText:
        index = line.rfind('|')
        quranWithSpaces.write(line[:index+1])
        quranWithSpaces.write(" ")
        quranWithSpaces.write(line[index+1:])