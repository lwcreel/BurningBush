from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#from gensim.summarization.bm25 import get_bm25_weights

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
bibleText = [word for word in bibleText if word not in stopwords.words('english')]
quranText = quran.read()
quranText = quranText.split(" ")
quranText = [word for word in quranText if word not in stopwords.words('english')]

# iterate through the lists, simplifying words and writing to output
for i in bibleText:    
    bibleOut.write(stemmer.stem(i))
    bibleOut.write(" ")

for i in quranText:
    quranOut.write(stemmer.stem(i))
    quranOut.write(" ")

bibleText = bibleOut.read().split(" ")
quranText = quran.read().split(" ")
corpus = [bibleText, quranText]
