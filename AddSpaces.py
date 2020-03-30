import re

quran = open("Docs/Quran.txt", "r")
quranWithSpaces = open("Docs/QuranWithSpaces.txt", "w")
# read data and split into words
quranText = quran.read()
quranText = quranText.split()

# create new Quran doc 
# (remove second pipe, add space after chapter|verse, add underscore after each verse)

index = 0
first = False
for word in quranText: 
    if (index != len(quranText)-1):
        if (re.match(r"[0-9]+\|[0-9]+\|", word)):
            if (first):
                quranWithSpaces.write("_ ") # adding _ to split verses up
            pipe_index = word.rfind('|') # second pipe
            quranWithSpaces.write(word[:pipe_index]) # write word up until second pip
            quranWithSpaces.write(" ") # add space
            quranWithSpaces.write(word[pipe_index+1:]) # write the rest of the word after second pipe
            quranWithSpaces.write(" ")
            first = True
        else:
            quranWithSpaces.write(word)
            quranWithSpaces.write(" ")
    else:
        quranWithSpaces.write(word)
    index += 1


# add space between chapter and verse of stemmed Quran (chapter| verse)
quran2 = open("Docs/StemmedQuran.txt", "r")
quranWithSpaces2 = open("Docs/StemmedQuranWithSpaces.txt", "w")
quranText2 = quran2.read()
quranText2 = quranText2.split()

for word in quranText2:
    if (re.match(r"^[0-9]+|[0-9]+$", word)): # if word is chapter|verse
        chapterVerse = word.split('|') # get chapter and verse number
        quranWithSpaces2.write(chapterVerse[0]) # write chapter number
        quranWithSpaces2.write('| ') # write pipe with space
        quranWithSpaces2.write(chapterVerse[1]) #write verse number
        quranWithSpaces2.write(" ")
    else:
        quranWithSpaces2.write(word) # write regular word followed by space
        quranWithSpaces2.write(" ")


