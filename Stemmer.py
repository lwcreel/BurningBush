from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

# create stemmer object to simplify
stemmer = PorterStemmer()

# open input files
bible = open("Docs/Bible.txt", "r")
quran = open("Docs/Quran.txt", "r")

# open output files
bibleOut = open("Docs/StemmedBible.txt", "w")
quranOut = open("Docs/StemmedQuran.txt", "w")

# read data and split into words
bibleText = bible.read()
bibleText = bibleText.split(" ")
quranText = quran.read()
quranText = quranText.split(" ")

# iterate through the lists, simplifying words and writing to output
for i in bibleText:
    bibleOut.write(stemmer.stem(i))
    bibleOut.write(" ")

for i in quranText:
    quranOut.write(stemmer.stem(i))
    quranOut.write(" ")
