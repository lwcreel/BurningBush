# have to do: pip install rank_bm25

import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

# functions
def CreateCorpus(file1, file2):
    corpus = []
    stemmedCorpus =[]
    doc = open("Docs/"+file1, "r")
    stemmedDoc = open("Docs/"+file2, "r")
    corpus = doc.read().split(" _ ") 
    stemmedCorpus = stemmedDoc.read().split(" _ ")
    return corpus, stemmedCorpus

def StemQuery(query):
    stemmer = PorterStemmer()
    pat = re.compile(r'[^A-Za-z0-9 \:]+')
    query = re.sub(pat, '', query).lower() # make query lowercase
    tokenized_query = query.split(" ") # split query by space
    tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')] # remove stop words from query
    stemmed_query = []
    for word in tokenized_query: # stem query
        word = stemmer.stem(word)
        stemmed_query.append(word)
    return stemmed_query


stemmer = PorterStemmer()

corpusB, stemmedCorpusB = CreateCorpus("BibleWithBookNames.txt","StemmedBibleWithBookNames.txt")
corpusQ, stemmedCorpusQ = CreateCorpus("quranWithSpaces.txt","StemmedQuran.txt")

oneVerse = False
book = "Psalms"
chapter = "22"
if (chapter != ""):
    chapter = chapter + ":"
verse = "12"
query = "loved"

if (book != "" and chapter != "" and verse != ""):
    stemmed_query = [book, chapter, verse]
    oneVerse = True
else:
    stemmed_query = StemQuery(query)
    if (chapter != ""):
        stemmed_query.insert(0, chapter)
    if (book != ""):
        stemmed_query.insert(0, book)
print(stemmed_query)

# could do the substring thing to make a new corpus and only search the smaller corpus if book and/or chapter
# corpusB = [i for i in corpusB if stemmed_query in i] 
# stemmed_query = book + " " + chapter
# stemmedCorpusB = [i for i in corpusB if stemmed_query in i] 
# print (stemmedCorpusB)

tokenized_corpus = [doc.split(" ") for doc in stemmedCorpusB]
bm25 = BM25Okapi(tokenized_corpus)

doc_scores = bm25.get_scores(stemmed_query) # get scores
doc_scores = list(doc_scores) # make doc_scores a list
doc_scores_sorted = sorted(doc_scores, reverse=True) # sort scores in decreasing order (highest score first)
# print (doc_scores)
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
# print(matches)

# all_results = bm25.get_top_n(tokenized_query, stemmedCorpusB, n=10)

results = [corpusB[i] for i in matches] # this holds the final results

if (len(results) == 0):
    print("No results found. Suggestions: make query more specific and check for misspellings.")
elif (oneVerse):
    subs = book + " " + chapter + verse
    results = [i for i in corpusB if subs in i] 
    if (len(results) == 0):
        print("No results found. Chapter or verse out of range.")
    else:
        print(*results, sep = "\n")
else:
    print(*results, sep = "\n")