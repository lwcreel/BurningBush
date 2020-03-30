# have to do: pip install rank_bm25

import re
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

# functions:
# creates both the regular corpus and the stemmed corpus by splitting by " _ "
def CreateCorpus(file1, file2):
    corpus = []
    stemmedCorpus =[]
    doc = open("Docs/"+file1, "r")
    stemmedDoc = open("Docs/"+file2, "r")
    corpus = doc.read().split(" _ ") 
    stemmedCorpus = stemmedDoc.read().split(" _ ")
    return corpus, stemmedCorpus

# cleans up the query and adds book/chapter to query if needed
def StemQuery(stemmer, query, doc, book, chapter):
    pat = re.compile(r'[^A-Za-z0-9 \:\|]+') # remove everything but letters, numbers, :, and |
    query = re.sub(pat, '', query).lower() # make query lowercase
    tokenized_query = query.split(" ") # split query by space
    tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')] # remove stop words from query
    stemmed_query = []
    for word in tokenized_query: # stem query
        word = stemmer.stem(word)
        stemmed_query.append(word)
    if (doc == "b"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter) # adds chapter in front of query if included
        if (book != ""):
            stemmed_query.insert(0, book) # adds book in front of query if included
    elif (doc == "q"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter) # adds chapter in front of query if included
    elif (doc == "x"): # can only search query when comparing so do nothing
        pass
    print(stemmed_query)
    return stemmed_query

# returns only one verse from the text
def OneVerse(query, doc):
    if (doc == "b"):
        results = [i for i in corpusB if query in i] 
    elif (doc == "q"):
        results = [i for i in corpusB if query in i] 
    return results

# uses BM25 on the stemmed corpus to give scores for each document in order to return the top <amt> of documents from corpus that are most relevant
def Search(stemmer, stemmed_query, corpus, stemmedCorpus, amt):
    tokenized_corpus = [doc.split(" ") for doc in stemmedCorpus] # split stemmedcorpus by space
    bm25 = BM25Okapi(tokenized_corpus) # run BM25 on tokenized stemmed corpus
    doc_scores = list(bm25.get_scores(stemmed_query)) # get scores of all the documents and make it a list
    doc_scores_sorted = sorted(doc_scores, reverse=True) # sort scores in decreasing order (highest score first)
    if (len(doc_scores_sorted) < amt): # it will find top <amt> results (or less)
        length = len(doc_scores_sorted)
    else:
        length = amt
    # have to translate stemmed corpus results to corpus results so we can return the nonstemmed results
    matches = []
    i = 0
    while (i < length and doc_scores_sorted[i] > 0):
        match = doc_scores.index(doc_scores_sorted[i])
        matches.append(match) # matches will contain the indices in corpus of the results with a score over 0
        doc_scores[match] = "done"
        i += 1
    results = [corpus[i] for i in matches] # this holds the final results from regular corpus
    return results


# main: 
# variables
results = []
resultsB = []
resultsQ = []
oneVerse = False 
both = False

stemmer = PorterStemmer()

# make corpus and stemmed corpus for both Bible and Quran
corpusB, stemmedCorpusB = CreateCorpus("BibleWithBookNames.txt", "StemmedBibleWithBookNames.txt")
corpusQ, stemmedCorpusQ = CreateCorpus("QuranWithSpaces.txt", "StemmedQuran.txt")

# user input / query section
doc = "b" # b for Bible, q for Quran, x for both
book = ""
chapter = ""
verse = ""
query = "loved you"

# separated based on the doc (b, q, or x)
if (doc == "b"):
    if (chapter != ""):
        chapter = chapter + ":" # add colon if they have chapter
    if (book != "" and chapter != "" and verse != ""): # if have all 3, only search for one verse
        oneVerse = True
        stemmed_query = book + " " + chapter + verse
        results = OneVerse(stemmed_query, "b")
    else: # regular search
        stemmed_query = StemQuery(stemmer, query, "b", book, chapter)
        results = Search(stemmer, stemmed_query, corpusB, stemmedCorpusB, 10)
elif (doc == "q"):
    if (chapter != ""):
        chapter = chapter + "|" # add pipe if they have chapter
    if (chapter != "" and verse != ""): # if have both, only search for one verse
        oneVerse = True
        stemmed_query = chapter + "|" + verse
        results = OneVerse(stemmer, stemmed_query, "q")
    else: # regular search
        stemmed_query = StemQuery(stemmer, query, "q", "", chapter)
        results = Search(stemmer, stemmed_query, corpusQ, stemmedCorpusQ, 10)
elif (doc == "x"):
    both = True
    stemmed_query = StemQuery(stemmer, query, "x", book, chapter)
    # if both, they can only search qith the query, so do a regular search for both
    resultsB = Search(stemmer, stemmed_query, corpusB, stemmedCorpusB, 5)
    resultsQ = Search(stemmer, stemmed_query, corpusQ, stemmedCorpusQ, 5)

if (oneVerse and len(results) == 0):
    print("No results found. Chapter or verse out of range.")
elif (both and len(resultsB) == 0 and len(resultsQ == 0)):
    print("No results found. Suggestions: make your query more specific and check for misspellings.")
elif (not oneVerse and not both and len(results) == 0):
    print("No results found. Suggestions: make your query more specific and check for misspellings.")
else:
    if (oneVerse):
        results = results[0] # only keep the very first result
        print(*results, sep = "")
    elif (both):
        print("Bible:")
        print(*resultsB, sep = "\n")
        print("\nQuran:")
        print(*resultsQ, sep = "\n")
    else:
        print(*results, sep = "\n")



# could do the substring thing to make a new corpus and only search the smaller corpus if book and/or chapter
# corpusB = [i for i in corpusB if stemmed_query in i] 
# stemmed_query = book + " " + chapter
# stemmedCorpusB = [i for i in corpusB if stemmed_query in i] 