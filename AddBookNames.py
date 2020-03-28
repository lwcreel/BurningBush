import re

# open Bible files
bible = open("Docs/Bible.txt", "r")
bibleWithBookNames = open("Docs/BibleWithBookNames.txt", "w")

# read data and split into words
# bible is King James Version (KJV)
bibleText = bible.read()
bibleText = bibleText.split()

first = False

index = 0
for word in bibleText:
    if (index != len(bibleText)-1):
        if (re.match(r"^1:1$", bibleText[index+1])): # current word is Bible book
            currBook = bibleText[index]
            # if (currBook != "Genesis"):
            #     bibleWithBookNames.write("!! ")
        elif (re.match(r"^[0-9]+:[0-9]+$", word)):
            if (first):
                bibleWithBookNames.write("_ ")
            bibleWithBookNames.write(currBook)
            bibleWithBookNames.write(" ")
            bibleWithBookNames.write(word)
            bibleWithBookNames.write(" ")
            first = True
        else:
            bibleWithBookNames.write(word)
            bibleWithBookNames.write(" ")
    else:
        bibleWithBookNames.write(word)
    index += 1


# books = ["Genesis‌","Exodus","Leviticus‌","Numbers‌","Deuteronomy","Joshua","‌Judges","‌Ruth","‌1Samuel‌‌","2Samuel","‌‌1Kings‌‌","2Kings‌‌","1Chronicles‌","2Chronicles‌","Ezra‌","Nehemiah","‌Esther","‌Job","‌Psalms‌","Proverbs","‌Ecclesiastes‌","SongofSolomon‌","Isaiah‌","Jeremiah","‌Lamentations‌","Ezekiel","‌Daniel‌","Hosea","‌Joel‌","Amos‌","Obadiah‌","Jonah","Micah","Nahum","‌Habakkuk","Zephaniah‌","‌Haggai‌","Zechariah","Malachi‌","Matthew‌","Mark","‌Luke‌","John","‌Acts‌","Romans‌","‌1‌Corinthians","2Corinthians‌","Galatians‌","Ephesians‌","Philippians‌","Colossians‌","1Thessalonians‌","2Thessalonians‌","1Timothy‌","2Timothy‌","Titus‌","Philemon‌","Hebrews‌","James","1Peter‌","2Peter","1John‌","2John‌","3John‌","Jude‌","Revelation"]

# bible = open("Docs/StemmedBible.txt", "r")
# bibleWithBookNames = open("Docs/StemmedBibleWithBookNames.txt", "w")

# # read data and split into words
# # bible is King James Version (KJV)
# bibleText = bible.read()
# bibleText = bibleText.split()

# index = 0
# for word in bibleText:
#     if (any(c.isupper() for c in word) and word != "Genesis"):
#         bibleWithBookNames.write("_ ")
#         bibleWithBookNames.write(word)
#         bibleWithBookNames.write(" ")
#     elif (re.match(r"^1:1$", word)):
#         currBook = bibleText[index-1]
#         chapterVerse = word.split(":") # split into words by :
#         bibleWithBookNames.write(chapterVerse[0])
#         bibleWithBookNames.write(": ")
#         bibleWithBookNames.write(chapterVerse[1])
#         bibleWithBookNames.write(" ")
#     elif (re.match(r"^[0-9]+:[0-9]+$", word)):
#         bibleWithBookNames.write("_ ")
#         bibleWithBookNames.write(currBook)
#         bibleWithBookNames.write(" ")
#         chapterVerse = word.split(":") # split into words by :
#         bibleWithBookNames.write(chapterVerse[0])
#         bibleWithBookNames.write(": ")
#         bibleWithBookNames.write(chapterVerse[1])
#         bibleWithBookNames.write(" ")
#     else:
#         bibleWithBookNames.write(word)
#         bibleWithBookNames.write(" ")
#     index += 1



  
