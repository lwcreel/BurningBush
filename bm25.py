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

def StemQuery(stemmer, query, doc, book, chapter):
    pat = re.compile(r'[^A-Za-z0-9 \:]+')
    query = re.sub(pat, '', query).lower() # make query lowercase
    tokenized_query = query.split(" ") # split query by space
    tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')] # remove stop words from query
    stemmed_query = []
    for word in tokenized_query: # stem query
        word = stemmer.stem(word)
        stemmed_query.append(word)
    if (doc == "b"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter)
        if (book != ""):
            stemmed_query.insert(0, book)
    elif (doc == "q"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter)
    print(stemmed_query)
    return stemmed_query

def OneVerse(query, doc):
    if (doc == "b"):
        results = [i for i in corpusB if query in i] 
    elif (doc == "q"):
        results = [i for i in corpusB if query in i] 
    return results

def Search(stemmer, stemmed_query, corpus, stemmedCorpus):
    tokenized_corpus = [doc.split(" ") for doc in stemmedCorpus]
    bm25 = BM25Okapi(tokenized_corpus)

    doc_scores = list(bm25.get_scores(stemmed_query)) # get scores and make it a list
    doc_scores_sorted = sorted(doc_scores, reverse=True) # sort scores in decreasing order (highest score first)
    
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

    results = [corpus[i] for i in matches] # this holds the final results
    return results
        

# main

stemmer = PorterStemmer()

corpusB, stemmedCorpusB = CreateCorpus("BibleWithBookNames.txt", "StemmedBibleWithBookNames.txt")
corpusQ, stemmedCorpusQ = CreateCorpus("quranWithSpaces.txt", "StemmedQuran.txt")

oneVerse = False
doc = "b"
book = ""
chapter = ""
verse = ""
query = "the lord said"

if (doc == "b"):
    if (chapter != ""):
        chapter = chapter + ":"
    if (book != "" and chapter != "" and verse != ""):
        stemmed_query = book + " " + chapter + verse
        results = OneVerse(stemmed_query, "b")
        oneVerse = True
    else:
        stemmed_query = StemQuery(stemmer, query, "b", book, chapter)
        results = Search(stemmer, stemmed_query, corpusB, stemmedCorpusB)
elif (doc == "q"):
    if (chapter != ""):
        chapter = chapter + "|"
    if (chapter != "" and verse != ""):
        stemmed_query = chapter + "|" + verse
        results = OneVerse(stemmer, stemmed_query, "q")
        oneVerse = True
    else:
        stemmed_query = StemQuery(stemmer, query, "q", book, chapter)
        results = Search(stemmer, stemmed_query, corpusQ, stemmedCorpusQ)

if (oneVerse and len(results) == 0):
    print("No results found. Chapter or verse out of range.")
elif (oneVerse):
    results = results[0]
    print(*results, sep = "")
elif (len(results) == 0):
    print("No results found. Suggestions: make your query more specific and check for misspellings.")
else:
    print(*results, sep = "\n")



# could do the substring thing to make a new corpus and only search the smaller corpus if book and/or chapter
# corpusB = [i for i in corpusB if stemmed_query in i] 
# stemmed_query = book + " " + chapter
# stemmedCorpusB = [i for i in corpusB if stemmed_query in i] 