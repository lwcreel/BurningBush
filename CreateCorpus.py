import re

corpusB = []
stemmedCorpusB =[]
corpusQ = []
stemmedCorpusQ =[]

# open Bible files
bible = open("Docs/BibleWithBookNames.txt", "r")
stemmedBible = open("Docs/StemmedBibleWithBookNames.txt", "r")

quran = open("Docs/quranWithSpaces.txt", "r")
stemmedQuran = open("Docs/StemmedQuran.txt", "r")

# read data and split by " _ " to store verses individually as "documents"
corpusB = bible.read().split(" _ ") 
stemmedCorpusB = stemmedBible.read().split(" _ ")
# random tests:
# print(corpusB[25000])
# print(stemmedCorpusB[25000])

corpusQ = quran.read().split(" _ ")
stemmedCorpusQ = stemmedQuran.read().split(" _ ")

print(corpusQ[500])
print(stemmedCorpusQ[500])
