import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

# all the books in the KJV bible
books = ["Genesis‌","Exodus","Leviticus‌","Numbers‌","Deuteronomy","Joshua","‌Judges","‌Ruth","‌1Samuel‌‌","2Samuel","‌‌1Kings‌‌","2Kings‌‌","1Chronicles‌","2Chronicles‌","Ezra‌","Nehemiah","‌Esther","‌Job","‌Psalms‌","Proverbs","‌Ecclesiastes‌","SongofSolomon‌","Isaiah‌","Jeremiah","‌Lamentations‌","Ezekiel","‌Daniel‌","Hosea","‌Joel‌","Amos‌","Obadiah‌","Jonah","Micah","Nahum","‌Habakkuk","Zephaniah‌","‌Haggai‌","Zechariah","Malachi‌","Matthew‌","Mark","‌Luke‌","John","‌Acts‌","Romans‌","‌1‌Corinthians","2Corinthians‌","Galatians‌","Ephesians‌","Philippians‌","Colossians‌","1Thessalonians‌","2Thessalonians‌","1Timothy‌","2Timothy‌","Titus‌","Philemon‌","Hebrews‌","James","1Peter‌","2Peter","1John‌","2John‌","3John‌","Jude‌","Revelation"]

#create stemmer object to simplify
stemmer = PorterStemmer()

# open input files
bible = open("Docs/Bible.txt", "r") # bible is King James Version (KJV)
quran = open("Docs/Quran.txt", "r")

# open output files
bibleOut = open("Docs/StemmedBible.txt", "w")
quranOut = open("Docs/StemmedQuran.txt", "w")

bibleText = bible.read() # read data
bibleText = bibleText.replace('\n', ' ') # replace new line with spaces
pat = re.compile(r'[^A-Za-z0-9 \:\_]+') # get rid of puncuation besides : and _
bibleText = re.sub(pat, '', bibleText)
bibleText = bibleText.split() # split into words by spaces

#iterate through the lists, simplifying words and writing to output
index = 0
# for word in bibleText:
#     if (index != len(bibleText)-1):
#         # if ("King_James_Bible" in word): # indicates it is the start of a testament (old/new), want to not stem and not lowercase
#         #     # bibleOut.write(word)
#         #     # bibleOut.write(" ")
#         #     pass # don't include testament names for now
#         if (re.match(r"^1:1$", bibleText[index+1])): # next word is 1:1 so current word is book chapter, want to not stem and not lowercase
#             bibleOut.write(word)
#             bibleOut.write(" ")
#         elif (re.match(r"[0-9]+:[0-9]+", word)): # is a chapter:verse
#             bibleOut.write(word)
#             bibleOut.write(" ")
#         elif (word.lower() in stopwords.words('english')): # don't include stop words
#             pass
#         else:
#             if ':' in word: # get rid of : that are a part of words
#                 word = word.replace(':','')
#             bibleOut.write(stemmer.stem(word.lower())) # stem word
#             bibleOut.write(" ")
#     else:
#         bibleOut.write(stemmer.stem(word.lower())) # stem the very last word
#     index += 1

quran_sp = open("Docs/QuranWithSpaces.txt")
#quranWithLines = open("Docs/quranWithLines.txt", "w")
quranText = quran_sp.read() # read data
#punct = re.compile(r'[^A-Za-z0-9 \|(\n)]+', re.MULTILINE) # get rid of puncuation |
punct = re.compile(r'[^A-Za-z0-9 \|\_]+') # get rid of puncuation |
quranText = re.sub(punct, '', quranText)
quranText = quranText.split()
quranText = [word.lower() for word in quranText]
#quranText = quranText.replace('\n', ' ') # replace new line with spaces
#quranText = quranText.splitlines(True) # split into words by spaces
#quranWithLines.writelines(quranText)


for word in quranText:
    if (word in stopwords.words('english')): # don't include stop words
        pass
    else:
        quranOut.write(stemmer.stem(word)) # stem word
        quranOut.write(" ")

# for line in quranText:
#     words=line.split()
#     for word in words:
#         if (word in stopwords.words('english')): # don't include stop words
#             pass
#         else:
#             quranOut.write(stemmer.stem(word)) # stem word
#             quranOut.write(" ")
#     quranOut.write("_")
#     quranOut.write("\n")   