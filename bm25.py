# have to do: pip install rank_bm25

import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

stemmer = PorterStemmer()

# not quite sure yet about what to do with BOOK CH:VRS part
corpusB = [
    "Genesis 1:1 In the beginning God created the heaven and the earth.",
    "Genesis 1:2 And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
    "Genesis 1:3 And God said, Let there be light: and there was light.",
    "Genesis 1:4 And God saw the light, that it was good: and God divided the light from the darkness.",
    "Genesis 1:5 And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day."
]

stemmedCorpusB = [
    "Genesis 1: 1 begin god creat heaven earth",
    "Genesis 1: 2 earth without form void dark upon face deep spirit god move upon face water",
    "Genesis 1: 3 god said let light light",
    "Genesis 1: 4 god saw light good god divid light dark",
    "Genesis 1: 5 god call light day dark call night even morn first day"
]



corpusB = []
stemmedCorpusB =[]
corpusQ = []
stemmedCorpusQ =[]
# open Bible files
bible = open("Docs/BibleWithBookNames.txt", "r")
stemmedBible = open("Docs/StemmedBibleWithBookNames.txt", "r")
# read data and split by " _ " to store verses individually as "documents"
corpusB = bible.read().split(" _ ") 
stemmedCorpusB = stemmedBible.read().split(" _ ")



tokenized_corpus = [doc.split(" ") for doc in stemmedCorpusB]
bm25 = BM25Okapi(tokenized_corpus)

book = "Psalms"
chapter = ""
if (chapter != ""):
    chapter = chapter + ":"
verse = ""
query = "love"

oneVerse = False

pat = re.compile(r'[^A-Za-z0-9 \:]+')
query = re.sub(pat, '', query).lower() # make query lowercase
tokenized_query = query.split(" ") # split query by space
tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')] # remove stop words from query
stemmed_query = [];
for word in tokenized_query: # stem query
    word = stemmer.stem(word)
    stemmed_query.append(word)
if (book != "" and chapter != "" and verse != ""):
    stemmed_query = [book, chapter, verse]
    oneVerse = True
else:
    if (chapter != ""):
        stemmed_query.insert(0, chapter)
    if (book != ""):
        stemmed_query.insert(0, book)

print(stemmed_query)

doc_scores = bm25.get_scores(stemmed_query) # get scores
doc_scores = list(doc_scores) # make doc_scores a list
# print (doc_scores)

doc_scores_sorted = sorted(doc_scores, reverse=True) # sort scores in decreasing order (highest score first)
# print(doc_scores_sorted)

if (len(doc_scores_sorted) < 10): # 10 here makes it to where it will find top 10 results (or less)
    length = len(doc_scores_sorted)
else:
    length = 10

matches = []
i = 0
while (i < length and doc_scores_sorted[i] > 0):
    match = doc_scores.index(doc_scores_sorted[i])
    matches.append(match) # matches will contain the indices of the results with a score over 0
    doc_scores[match] = "done"
    i += 1

# print("matches: ", matches)

# all_results = bm25.get_top_n(tokenized_query, stemmedCorpusB, n=10)

results = [corpusB[i] for i in matches] # this holds the final results


if (len(results) == 0):
        print("No results found. Suggestions: make query more specific and check for misspellings.")
elif (oneVerse):
    print(results[0])
else:
    print(*results, sep = "\n")