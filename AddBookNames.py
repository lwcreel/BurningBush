import re

# open Bible file
bible = open("Docs/StemmedBible.txt", "r")
bibleWithBookNames = open("Docs/StemmedBibleWithBookNames.txt", "w")

# read data and split into words
# bible is King James Version (KJV)
bibleText = bible.read()
bibleText = bibleText.split()

index = 0
for word in bibleText:
    if (re.match(r"^1:1$", word)):
        currBook = bibleText[index-1]
    elif (re.match(r"^[0-9]+:[0-9]+$", word)):
        bibleWithBookNames.write(currBook)
        bibleWithBookNames.write(" ")
    bibleWithBookNames.write(word)
    bibleWithBookNames.write(" ")
    index += 1