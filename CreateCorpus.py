import re

corpusB = []
stemmedCorpusB =[]
corpusQ = []
stemmedCorpusQ =[]

# open Bible files
bible = open("Docs/BibleWithBookNames.txt", "r")
stemmedBible = open("Docs/StemmedBibleWithBookNames.txt", "r")

# quran = open("Docs/Quran.txt", "r")
# stemmedQuran = open("Docs/StemmedQuran.txt", "r")

# read data and split by " _ " to store verses individually as "documents"
corpusB = bible.read().split(" _ ") 
stemmedCorpusB = stemmedBible.read().split(" _ ")
# random tests:
# print(corpusB[20321])
# print(stemmedCorpusB[20321])

# quranText = quran.read() # read data
# quranText = quranText.split() # split into words by spaces
